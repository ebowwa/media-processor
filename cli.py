#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from src.video.extractor import VideoFrameExtractor
from src.image.upscaler import ImageUpscaler
from src.converters.webp_converter import WebPConverter


def main():
    parser = argparse.ArgumentParser(
        description="Media Processor - A unified tool for video and image processing"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Video to frames command
    video_parser = subparsers.add_parser('video2frames', help='Extract frames from video files')
    video_parser.add_argument('input', help='Input video file or directory')
    video_parser.add_argument('-o', '--output', help='Output directory for frames', default='frames')
    video_parser.add_argument('-r', '--rate', type=int, default=1, help='Frame extraction rate (seconds between frames)')
    video_parser.add_argument('--keep-video', action='store_true', help='Keep original video after extraction')
    
    # Image upscaling command
    upscale_parser = subparsers.add_parser('upscale', help='Upscale images using AI models')
    upscale_parser.add_argument('input', help='Input image file or directory')
    upscale_parser.add_argument('-o', '--output', help='Output file or directory')
    upscale_parser.add_argument('-m', '--model', default='modelx2', 
                              choices=['modelx2', 'modelx2_25_JXL', 'modelx4', 'minecraft_modelx4'],
                              help='Upscaling model to use')
    
    # WebP to PNG conversion command
    webp_parser = subparsers.add_parser('webp2png', help='Convert WebP images to PNG format')
    webp_parser.add_argument('input', help='Input WebP file or directory')
    webp_parser.add_argument('-o', '--output', help='Output PNG file or directory')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'video2frames':
            extractor = VideoFrameExtractor(frame_interval_seconds=args.rate)
            extractor.process(args.input, args.output, keep_video=args.keep_video)
            
        elif args.command == 'upscale':
            upscaler = ImageUpscaler(model_name=args.model)
            upscaler.process(args.input, args.output)
            
        elif args.command == 'webp2png':
            converter = WebPConverter()
            converter.process(args.input, args.output)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()