#!/usr/bin/env python3
"""Simple test script to verify the media processor CLI works correctly."""

import subprocess
import sys
from pathlib import Path


def test_cli_help():
    """Test that the CLI shows help."""
    result = subprocess.run([sys.executable, "cli.py", "-h"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Media Processor" in result.stdout
    print("✓ CLI help works")


def test_video2frames_help():
    """Test video2frames subcommand help."""
    result = subprocess.run([sys.executable, "cli.py", "video2frames", "-h"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Extract frames from video" in result.stdout
    print("✓ video2frames help works")


def test_upscale_help():
    """Test upscale subcommand help."""
    result = subprocess.run([sys.executable, "cli.py", "upscale", "-h"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Upscale images" in result.stdout
    print("✓ upscale help works")


def test_webp2png_help():
    """Test webp2png subcommand help."""
    result = subprocess.run([sys.executable, "cli.py", "webp2png", "-h"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Convert WebP" in result.stdout
    print("✓ webp2png help works")


def main():
    print("Testing Media Processor CLI...")
    
    try:
        test_cli_help()
        test_video2frames_help()
        test_upscale_help()
        test_webp2png_help()
        
        print("\nAll tests passed! ✓")
        print("\nTo test with actual files:")
        print("1. Video extraction: python cli.py video2frames your_video.mp4")
        print("2. Image upscaling: python cli.py upscale examples/example_1.png")
        print("3. WebP conversion: python cli.py webp2png your_image.webp")
        
    except AssertionError as e:
        print(f"\nTest failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()