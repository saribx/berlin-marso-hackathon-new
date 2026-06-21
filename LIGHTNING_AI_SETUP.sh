#!/bin/bash
# Quick setup for Lightning AI H100 environment

echo "================================================================================"
echo "LIGHTNING AI H100 - MARSO HACKATHON SETUP"
echo "================================================================================"

# Install kagglehub for downloading demos
echo "Installing kagglehub..."
pip install -q kagglehub

# Check if demos exist, if not download
if [ ! -f "il/demos/easy/trajectory.state.pd_ee_delta_pos.physx_cuda.h5" ]; then
    echo "Downloading demos..."
    python il/download_demos.py
    echo "✓ Demos downloaded"
else
    echo "✓ Demos already exist"
fi

echo ""
echo "================================================================================"
echo "SETUP COMPLETE!"
echo "================================================================================"
echo ""
echo "Now run:"
echo "  python il/train.py method=dp demo_dir=easy"
echo ""
echo "Or for the next iteration if needed:"
echo "  python il/train.py method=dp_fast demo_dir=easy"
echo ""
echo "================================================================================"
