# Media Processor

A unified Python tool for video and image processing, combining video frame extraction, AI-powered image upscaling, and WebP to PNG conversion.

## Features

- **Video Frame Extraction**: Extract frames from video files at specified intervals
- **Image Upscaling**: Upscale images using ONNX AI models (2x, 2.25x, 4x scaling)
- **WebP to PNG Conversion**: Convert WebP images to PNG format

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ebowwa/media-processor.git
cd media-processor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The tool provides a unified CLI interface for all operations:

### Video Frame Extraction

Extract frames from a video file:
```bash
python cli.py video2frames input_video.mp4 -o output_frames/
```

Extract frames from all videos in a directory:
```bash
python cli.py video2frames videos_directory/ -o frames_output/
```

Options:
- `-r, --rate`: Frame extraction rate in seconds (default: 1 second)
- `--keep-video`: Keep original video files after extraction

### Image Upscaling

Upscale a single image:
```bash
python cli.py upscale image.png -o upscaled_image.png
```

Upscale all images in a directory:
```bash
python cli.py upscale images_folder/ -o upscaled_folder/
```

Options:
- `-m, --model`: Choose upscaling model
  - `modelx2`: 2x upscaling (default)
  - `modelx2_25_JXL`: 2.25x upscaling
  - `modelx4`: 4x upscaling
  - `minecraft_modelx4`: 4x upscaling optimized for pixel art

### WebP to PNG Conversion

Convert a single WebP image:
```bash
python cli.py webp2png image.webp -o image.png
```

Convert all WebP images in a directory:
```bash
python cli.py webp2png webp_folder/ -o png_folder/
```

## Examples

1. Extract frames from a video every 2 seconds:
```bash
python cli.py video2frames movie.mp4 -r 2 -o movie_frames/
```

2. Upscale an image by 4x:
```bash
python cli.py upscale photo.jpg -m modelx4 -o photo_4x.jpg
```

3. Batch convert WebP images:
```bash
python cli.py webp2png downloads/ -o converted_pngs/
```

## Supported Formats

- **Video formats**: MP4, AVI, MOV, MKV
- **Image formats**: PNG, JPG, JPEG, BMP, TIFF (for upscaling)
- **Conversion**: WebP to PNG

## Requirements

- Python 3.7+
- OpenCV (cv2)
- NumPy
- Pillow (PIL)
- ONNX Runtime

## Project Structure

```
media-processor/
├── cli.py                 # Main CLI interface
├── requirements.txt       # Python dependencies
├── models/               # AI upscaling models
│   ├── modelx2.ort
│   ├── modelx2_25_JXL.ort
│   ├── modelx4.ort
│   └── minecraft_modelx4.ort
├── src/
│   ├── video/
│   │   └── extractor.py   # Video frame extraction
│   ├── image/
│   │   └── upscaler.py    # Image upscaling
│   └── converters/
│       └── webp_converter.py  # WebP to PNG conversion
└── examples/             # Example files
```

## License

This project consolidates functionality from:
- Video2Img
- upscale_img
- webp2png

Please refer to the original repositories for specific licensing information.