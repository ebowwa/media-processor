import cv2
import os
from pathlib import Path
from typing import Optional, Union


class VideoFrameExtractor:
    def __init__(self, frame_interval_seconds: int = 1, max_frames: int = 5000):
        self.frame_interval_seconds = frame_interval_seconds
        self.max_frames = max_frames
    
    def extract_frames(self, video_path: str, output_dir: str) -> int:
        """Extract frames from a single video file."""
        video_path = Path(video_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        vidcap = cv2.VideoCapture(str(video_path))
        fps = int(vidcap.get(cv2.CAP_PROP_FPS))
        
        if fps == 0:
            raise ValueError(f"Could not determine FPS for video: {video_path}")
        
        frame_interval = fps * self.frame_interval_seconds
        
        count = 0
        saved_count = 0
        success = True
        
        print(f"Processing video: {video_path.name}")
        print(f"FPS: {fps}, extracting 1 frame every {self.frame_interval_seconds} seconds")
        
        while success and count < self.max_frames:
            success, image = vidcap.read()
            
            if success and count % frame_interval == 0:
                frame_filename = output_dir / f"{video_path.stem}_frame{saved_count + 1}.jpg"
                cv2.imwrite(str(frame_filename), image)
                
                if frame_filename.stat().st_size > 0:
                    saved_count += 1
                    print(f"Saved frame {saved_count}")
                else:
                    frame_filename.unlink()
                    print(f"Failed to save frame at count {count}")
            
            count += 1
        
        vidcap.release()
        print(f"Extracted {saved_count} frames from {video_path.name}")
        return saved_count
    
    def process(self, input_path: Union[str, Path], output_dir: Union[str, Path], 
                keep_video: bool = False) -> None:
        """Process video file(s) from input path."""
        input_path = Path(input_path)
        output_dir = Path(output_dir)
        
        if input_path.is_file():
            # Single file processing
            if input_path.suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']:
                self.extract_frames(str(input_path), str(output_dir))
                if not keep_video:
                    input_path.unlink()
                    print(f"Deleted original video: {input_path}")
            else:
                raise ValueError(f"Unsupported video format: {input_path.suffix}")
        
        elif input_path.is_dir():
            # Directory processing
            video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
            video_files = [f for f in input_path.iterdir() 
                          if f.suffix.lower() in video_extensions]
            
            if not video_files:
                print(f"No video files found in {input_path}")
                return
            
            for video_file in video_files:
                video_output_dir = output_dir / video_file.stem
                self.extract_frames(str(video_file), str(video_output_dir))
                
                if not keep_video:
                    video_file.unlink()
                    print(f"Deleted original video: {video_file}")
        
        else:
            raise ValueError(f"Input path does not exist: {input_path}")