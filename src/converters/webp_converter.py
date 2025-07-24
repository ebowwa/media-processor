from PIL import Image
from pathlib import Path
from typing import Union, Optional


class WebPConverter:
    def convert_webp_to_png(self, source_path: Union[str, Path], target_path: Union[str, Path]) -> None:
        """Convert a single WebP image to PNG format."""
        source_path = Path(source_path)
        target_path = Path(target_path)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        if source_path.suffix.lower() != '.webp':
            raise ValueError(f"Input file is not a WebP image: {source_path}")
        
        # Ensure target directory exists
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert the image
        with Image.open(source_path) as img:
            img.save(target_path, 'PNG')
        
        print(f"Converted {source_path.name} to {target_path.name}")
    
    def process(self, input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> None:
        """Process WebP file(s) from input path."""
        input_path = Path(input_path)
        
        if input_path.is_file():
            # Single file processing
            if output_path is None:
                output_path = input_path.with_suffix('.png')
            else:
                output_path = Path(output_path)
                if output_path.is_dir():
                    output_path = output_path / input_path.with_suffix('.png').name
            
            self.convert_webp_to_png(input_path, output_path)
        
        elif input_path.is_dir():
            # Directory processing
            if output_path is None:
                output_path = input_path.parent / f"{input_path.name}_png"
            else:
                output_path = Path(output_path)
            
            output_path.mkdir(parents=True, exist_ok=True)
            
            webp_files = list(input_path.glob('*.webp')) + list(input_path.glob('*.WEBP'))
            
            if not webp_files:
                print(f"No WebP files found in {input_path}")
                return
            
            print(f"Found {len(webp_files)} WebP files to convert")
            
            for webp_file in webp_files:
                try:
                    target_file = output_path / webp_file.with_suffix('.png').name
                    self.convert_webp_to_png(webp_file, target_file)
                except Exception as e:
                    print(f"Error converting {webp_file}: {e}")
        
        else:
            raise ValueError(f"Input path does not exist: {input_path}")