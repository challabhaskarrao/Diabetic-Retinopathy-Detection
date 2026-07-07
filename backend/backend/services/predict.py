import time
import torch
import torch.nn.functional as F
import numpy as np
from PIL import Image

import sys
import os
# Ensure training package is in path to load the model
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from training.model import create_dr_model
from training.augmentations import get_val_transforms

class Predictor:
    def __init__(self, model_path=None, device=None):
        self.device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = create_dr_model(pretrained=False) # Architecture only
        self.transforms = get_val_transforms()
        
        # Mapping numerical grades to strings
        self.grade_map = {
            0: "No DR",
            1: "Mild",
            2: "Moderate",
            3: "Severe",
            4: "Proliferative DR"
        }
        
        # Load weights if provided, else use dummy weights for API structure testing
        if model_path and os.path.exists(model_path):
            checkpoint = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            print(f"Loaded model from {model_path}")
        else:
            print("Warning: No model weights found. Using uninitialized weights for prediction.")
            
        self.model.to(self.device)
        self.model.eval()
        
    def predict(self, image_np: np.ndarray):
        """
        Runs inference on a preprocessed NumPy image array.
        Returns prediction, confidence, probabilities, and processing time.
        """
        start_time = time.time()
        
        # Apply validation transforms (Resize, Normalize, ToTensor)
        augmented = self.transforms(image=image_np)
        input_tensor = augmented['image'].unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            output = self.model(input_tensor)
            probs = F.softmax(output, dim=1).squeeze().cpu().numpy()
            
        end_time = time.time()
        
        grade = int(np.argmax(probs))
        confidence = float(probs[grade])
        processing_time = end_time - start_time
        
        # Convert probabilities to a clean list of floats
        probabilities_list = [float(p) for p in probs]
        
        return {
            "prediction": self.grade_map[grade],
            "grade": grade,
            "confidence": confidence,
            "probabilities": probabilities_list,
            "processing_time": processing_time
        }
