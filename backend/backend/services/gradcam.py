import cv2
import numpy as np
import torch
import torch.nn.functional as F

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.feature_maps = None
        self.gradients = None
        
        # Register hooks
        self._register_hooks()
        
    def _save_feature_maps(self, module, input, output):
        self.feature_maps = output.detach()
        
    def _save_gradients(self, module, grad_in, grad_out):
        self.gradients = grad_out[0].detach()
        
    def _register_hooks(self):
        # Register forward hook to get feature maps
        self.target_layer.register_forward_hook(self._save_feature_maps)
        # Register backward hook to get gradients
        self.target_layer.register_full_backward_hook(self._save_gradients)
        
    def generate_heatmap(self, input_image, class_idx=None):
        """
        Generates the Grad-CAM heatmap for a given input image.
        input_image: Tensor of shape (1, 3, H, W)
        """
        self.model.eval()
        self.model.zero_grad()
        
        # Forward pass
        output = self.model(input_image)
        
        if class_idx is None:
            class_idx = output.argmax(dim=1).item()
            
        # Target for backprop
        target = output[0, class_idx]
        target.backward()
        
        # Pool the gradients across the spatial dimensions
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        
        # Weight the feature maps by the pooled gradients
        for i in range(self.feature_maps.shape[1]):
            self.feature_maps[:, i, :, :] *= pooled_gradients[i]
            
        # Average the weighted feature maps along the channel dimension
        heatmap = torch.mean(self.feature_maps, dim=1).squeeze()
        
        # ReLU to keep only features that have a positive influence on the class
        heatmap = F.relu(heatmap)
        
        # Normalize between 0 and 1
        heatmap /= torch.max(heatmap)
        
        return heatmap.cpu().numpy()
        
    @staticmethod
    def overlay_heatmap(original_image, heatmap, alpha=0.5, colormap=cv2.COLORMAP_JET):
        """
        Overlays the generated heatmap on the original image.
        original_image: numpy array (H, W, 3) in RGB format
        heatmap: numpy array (H', W') with values in [0, 1]
        """
        # Resize heatmap to match original image size
        heatmap = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
        
        # Convert heatmap to RGB using the colormap
        heatmap_uint8 = np.uint8(255 * heatmap)
        heatmap_colored = cv2.applyColorMap(heatmap_uint8, colormap)
        heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
        
        # Superimpose the heatmap on original image
        superimposed_img = cv2.addWeighted(original_image, 1 - alpha, heatmap_colored, alpha, 0)
        return superimposed_img
