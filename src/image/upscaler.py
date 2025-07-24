import numpy as np
import cv2
import onnxruntime
from PIL import Image
from pathlib import Path
from typing import Union, Optional


class ImageUpscaler:
    def __init__(self, model_name: str = "modelx2"):
        self.model_name = model_name
        self.model_path = None
        self._validate_model()
    
    def _validate_model(self):
        """Validate and set the model path."""
        models_dir = Path(__file__).parent.parent.parent / "models"
        self.model_path = models_dir / f"{self.model_name}.ort"
        
        if not self.model_path.exists():
            available_models = [f.stem for f in models_dir.glob("*.ort")]
            raise ValueError(f"Model '{self.model_name}' not found. Available models: {available_models}")
    
    def _pre_process(self, img: np.ndarray) -> np.ndarray:
        """Pre-process image for model input."""
        # H, W, C -> C, H, W
        img = np.transpose(img[:, :, 0:3], (2, 0, 1))
        # C, H, W -> 1, C, H, W
        img = np.expand_dims(img, axis=0).astype(np.float32)
        return img
    
    def _post_process(self, img: np.ndarray) -> np.ndarray:
        """Post-process model output."""
        # 1, C, H, W -> C, H, W
        img = np.squeeze(img)
        # C, H, W -> H, W, C
        img = np.transpose(img, (1, 2, 0))[:, :, ::-1].astype(np.uint8)
        return img
    
    def _inference(self, img_array: np.ndarray) -> np.ndarray:
        """Run inference with the ONNX model."""
        options = onnxruntime.SessionOptions()
        options.intra_op_num_threads = 1
        options.inter_op_num_threads = 1
        
        ort_session = onnxruntime.InferenceSession(str(self.model_path), options)
        ort_inputs = {ort_session.get_inputs()[0].name: img_array}
        ort_outs = ort_session.run(None, ort_inputs)
        
        return ort_outs[0]
    
    def _convert_pil_to_cv2(self, image: Image.Image) -> np.ndarray:
        """Convert PIL image to OpenCV format."""
        open_cv_image = np.array(image)
        # RGB to BGR
        if len(open_cv_image.shape) == 3:
            open_cv_image = open_cv_image[:, :, ::-1].copy()
        return open_cv_image
    
    def upscale_image(self, image_path: Union[str, Path]) -> np.ndarray:
        """Upscale a single image."""
        image_path = Path(image_path)
        if not image_path.exists():
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Load image
        image = Image.open(image_path)
        img = self._convert_pil_to_cv2(image)
        
        # Handle grayscale images
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        
        # Handle images with alpha channel
        if img.shape[2] == 4:
            alpha = img[:, :, 3]  # GRAY
            alpha = cv2.cvtColor(alpha, cv2.COLOR_GRAY2BGR)  # BGR
            alpha_output = self._post_process(self._inference(self._pre_process(alpha)))  # BGR
            alpha_output = cv2.cvtColor(alpha_output, cv2.COLOR_BGR2GRAY)  # GRAY
            
            img_rgb = img[:, :, 0:3]  # BGR
            image_output = self._post_process(self._inference(self._pre_process(img_rgb)))  # BGR
            image_output = cv2.cvtColor(image_output, cv2.COLOR_BGR2BGRA)  # BGRA
            image_output[:, :, 3] = alpha_output
        else:
            # Regular RGB image
            image_output = self._post_process(self._inference(self._pre_process(img)))
        
        return image_output
    
    def process(self, input_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None) -> None:
        """Process image file(s) from input path."""
        input_path = Path(input_path)
        
        if input_path.is_file():
            # Single file processing
            if output_path is None:
                output_path = input_path.parent / f"{input_path.stem}_upscaled{input_path.suffix}"
            else:
                output_path = Path(output_path)
            
            print(f"Upscaling image: {input_path}")
            upscaled = self.upscale_image(input_path)
            cv2.imwrite(str(output_path), upscaled)
            print(f"Saved upscaled image: {output_path}")
        
        elif input_path.is_dir():
            # Directory processing
            if output_path is None:
                output_path = input_path.parent / f"{input_path.name}_upscaled"
            else:
                output_path = Path(output_path)
            
            output_path.mkdir(parents=True, exist_ok=True)
            
            image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']
            image_files = [f for f in input_path.iterdir() 
                          if f.suffix.lower() in image_extensions]
            
            if not image_files:
                print(f"No image files found in {input_path}")
                return
            
            for image_file in image_files:
                try:
                    output_file = output_path / f"{image_file.stem}_upscaled{image_file.suffix}"
                    print(f"Upscaling: {image_file.name}")
                    upscaled = self.upscale_image(image_file)
                    cv2.imwrite(str(output_file), upscaled)
                    print(f"Saved: {output_file.name}")
                except Exception as e:
                    print(f"Error processing {image_file}: {e}")
        
        else:
            raise ValueError(f"Input path does not exist: {input_path}")