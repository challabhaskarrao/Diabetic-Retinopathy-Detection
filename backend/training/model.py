import torch
import torch.nn as nn
import timm

def create_dr_model(model_name="efficientnet_b3", num_classes=5, pretrained=True):
    """
    Creates an EfficientNet-B3 model for Diabetic Retinopathy classification.
    Uses timm (PyTorch Image Models) for pretrained weights.
    Replaces the final classification layer with `num_classes` outputs.
    """
    # Create the model using timm
    model = timm.create_model(model_name, pretrained=pretrained, num_classes=num_classes)
    
    # Optionally, we could add Dropout or a custom head here if needed,
    # but timm handles the replacement of the final FC layer automatically
    # when num_classes is specified.
    
    return model

if __name__ == "__main__":
    # Test model creation
    model = create_dr_model()
    print(model)
    
    # Test forward pass
    dummy_input = torch.randn(1, 3, 300, 300)
    output = model(dummy_input)
    print(f"Output shape: {output.shape}") # Should be (1, 5)
