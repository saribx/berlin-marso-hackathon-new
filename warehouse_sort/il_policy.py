"""Imitation-learning policy entrypoints for eval.py / the judge.

Each function satisfies the policy contract:
    policy.act(obs, deterministic=True) -> Tensor (num_envs, action_dim) in [-1, 1]

Wire one in via the config `policy` field:
    pixi run python eval.py difficulty=easy \\
        policy=warehouse_sort.il_policy:load_dp \\
        checkpoint=<path> eval_config=conf/eval/default.yaml

  load_dp      — state Diffusion Policy (main track; one checkpoint PER level)
  load_dp_rgb  — RGB Diffusion Policy (optional image track; template)
"""

import torch


def _add_baseline_path(rel):
    import os, sys
    p = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "il", "baselines", rel))
    if p not in sys.path:
        sys.path.insert(0, p)


# --------------------------------------------------------------------------- #
# State Diffusion Policy (MAIN track) — privileged low-dim state obs. Deployed fully
# closed-loop: re-query every step, execute the first predicted action. The state vector
# is parcel-count-specific, so a checkpoint is trained PER difficulty level.
# --------------------------------------------------------------------------- #
class _DPPolicy:
    def __init__(self, net, scheduler, obs_horizon, pred_horizon, act_dim, device,
                 num_inference_steps=16, act_horizon=8):
        self.net = net.to(device).eval()
        self.scheduler = scheduler
        self.scheduler.set_timesteps(num_inference_steps, device=device)
        self.obs_horizon = obs_horizon
        self.pred_horizon = pred_horizon
        self.act_dim = act_dim
        self.device = device
        self.prev = None
        self.act_horizon = act_horizon
        self.action_queue = []
        self.obs_history = []

    @torch.no_grad()
    def act(self, obs, deterministic=True):
        cur = (obs["state"] if isinstance(obs, dict) else obs).float().to(self.device)
        
        # Reset / initialize history and queue on reset or shape change
        # At reset, joint positions are START_QPOS, joint velocities are 0.
        start_qpos = torch.tensor([0.0, 0.3927, 0.0, -1.9635, 0.0, 2.356, 0.7854, 0.04, 0.04], device=cur.device)
        is_reset = torch.all(torch.abs(cur[:, 9:18]) < 1e-4, dim=1) & torch.all(torch.abs(cur[:, 0:9] - start_qpos) < 1e-3, dim=1)
        
        if torch.any(is_reset) or self.prev is None or self.prev.shape != cur.shape:
            self.obs_history = [cur] * self.obs_horizon
            self.action_queue = []
        else:
            self.obs_history.append(cur)
            if len(self.obs_history) > self.obs_horizon:
                self.obs_history.pop(0)
        self.prev = cur

        # If we have actions in the queue, return the next one
        if len(self.action_queue) > 0:
            return self.action_queue.pop(0)

        # Build global conditioning from history
        obs_cond = torch.stack(self.obs_history, dim=1).flatten(start_dim=1)
        B = cur.shape[0]
        naction = torch.randn((B, self.pred_horizon, self.act_dim), device=self.device)
        for k in self.scheduler.timesteps:
            noise_pred = self.net(sample=naction, timestep=k, global_cond=obs_cond)
            naction = self.scheduler.step(model_output=noise_pred, timestep=k, sample=naction).prev_sample
            
        start = self.obs_horizon - 1
        end = start + self.act_horizon
        actions = naction[:, start:end].clamp(-1.0, 1.0) # (B, act_horizon, act_dim)
        
        self.action_queue = [actions[:, i] for i in range(1, self.act_horizon)]
        return actions[:, 0]



def load_dp(checkpoint, sample_obs, action_space, device,
            obs_horizon=2, pred_horizon=16, diffusion_step_embed_dim=64,
            unet_dims=(64, 128, 256), n_groups=8, num_diffusion_iters=100,
            num_inference_steps=30, act_horizon=8):
    """Load a state Diffusion Policy checkpoint (uses EMA weights).

    ORGANIZER FIX: num_inference_steps increased to 30 for steadier actions.
    """
    _add_baseline_path("diffusion_policy")
    from diffusion_policy.conditional_unet1d import ConditionalUnet1D
    from diffusers.schedulers.scheduling_ddpm import DDPMScheduler

    state = sample_obs["state"] if isinstance(sample_obs, dict) else sample_obs
    obs_dim = state.shape[1]
    act_dim = action_space.shape[0]
    net = ConditionalUnet1D(
        input_dim=act_dim, global_cond_dim=obs_horizon * obs_dim,
        diffusion_step_embed_dim=diffusion_step_embed_dim,
        down_dims=list(unet_dims), n_groups=n_groups,
    )
    ckpt = torch.load(checkpoint, map_location=device, weights_only=False)
    sd = ckpt.get("ema_agent", ckpt.get("agent"))
    net_sd = {k.replace("noise_pred_net.", "", 1): v for k, v in sd.items()
              if k.startswith("noise_pred_net.")}
    net.load_state_dict(net_sd)
    scheduler = DDPMScheduler(num_train_timesteps=num_diffusion_iters,
                              beta_schedule="squaredcos_cap_v2", clip_sample=True,
                              prediction_type="epsilon")
    return _DPPolicy(net, scheduler, obs_horizon, pred_horizon, act_dim, device,
                     num_inference_steps=num_inference_steps, act_horizon=act_horizon)


# --------------------------------------------------------------------------- #
# RGB Diffusion Policy (OPTIONAL image track) — image + robot proprioception, NO privileged state.
# Same fixed image input shape at every difficulty; same checkpoint runs across configs.
# Template only — image IL is not yet solving this task.
# --------------------------------------------------------------------------- #
class _DPRgbPolicy:
    def __init__(self, agent, obs_horizon, device, num_inference_steps=16):
        self.agent = agent.to(device).eval()
        self.agent.noise_scheduler.set_timesteps(num_inference_steps)
        self.obs_horizon = obs_horizon
        self.device = device
        self.prev_state = None
        self.state_hist = None
        self.rgb_hist = None

    @torch.no_grad()
    def act(self, obs, deterministic=True):
        state = obs["state"].float().to(self.device)
        rgb = obs["rgb"].to(self.device)
        if self.prev_state is None or self.prev_state.shape != state.shape:
            self.state_hist = [state] * self.obs_horizon
            self.rgb_hist = [rgb] * self.obs_horizon
        else:
            self.state_hist = self.state_hist[1:] + [state]
            self.rgb_hist = self.rgb_hist[1:] + [rgb]
        self.prev_state = state

        obs_seq = {
            "state": torch.stack(self.state_hist, dim=1),
            "rgb": torch.stack(self.rgb_hist, dim=1),
        }
        aseq = self.agent.get_action(obs_seq)
        return aseq[:, 0].clamp(-1.0, 1.0)


def load_dp_rgb(checkpoint, sample_obs, action_space, device,
                obs_horizon=2, act_horizon=8, pred_horizon=16,
                diffusion_step_embed_dim=64, unet_dims=(64, 128, 256), n_groups=8,
                num_inference_steps=16, visual_encoder="plain_conv", num_kp=32):
    """Load an RGB Diffusion Policy checkpoint (vendored train_rgbd; uses EMA weights).

    Template implementation — image IL is not yet solving this task.
    """
    import types
    import numpy as np
    import gymnasium.spaces as spaces
    _add_baseline_path("diffusion_policy")
    from train_rgbd import Agent

    h, w, c = sample_obs["rgb"].shape[1:]
    state_dim = sample_obs["state"].shape[1]
    stub = types.SimpleNamespace(
        single_observation_space=spaces.Dict({
            "state": spaces.Box(-np.inf, np.inf, (obs_horizon, state_dim), np.float32),
            "rgb": spaces.Box(0, 255, (obs_horizon, h, w, c), np.uint8),
        }),
        single_action_space=spaces.Box(-1.0, 1.0, (action_space.shape[0],), np.float32),
    )
    args = types.SimpleNamespace(
        obs_horizon=obs_horizon, act_horizon=act_horizon, pred_horizon=pred_horizon,
        diffusion_step_embed_dim=diffusion_step_embed_dim, unet_dims=list(unet_dims),
        n_groups=n_groups, visual_encoder=visual_encoder, num_kp=num_kp,
    )
    agent = Agent(stub, args)
    ckpt = torch.load(checkpoint, map_location=device, weights_only=False)
    agent.load_state_dict(ckpt.get("ema_agent", ckpt.get("agent")))
    return _DPRgbPolicy(agent, obs_horizon, device, num_inference_steps=num_inference_steps)
