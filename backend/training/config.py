import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class TrainingConfig:
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = BASE_DIR / "datasets"
    CHECKPOINT_DIR: Path = BASE_DIR / "checkpoints"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # Model configuration
    MODEL_NAME: str = "efficientnet_b3"
    NUM_CLASSES: int = 5
    PRETRAINED: bool = True
    
    # Training parameters
    BATCH_SIZE: int = 32
    EPOCHS: int = 50
    LEARNING_RATE: float = 3e-4
    WEIGHT_DECAY: float = 1e-4
    NUM_WORKERS: int = 4
    
    # Image parameters
    IMAGE_SIZE: int = 300  # EfficientNet-B3 default is typically 300x300
    
    # Augmentation parameters
    MIXED_PRECISION: bool = True
    GRADIENT_CLIPPING: float = 1.0
    
    # Early stopping
    PATIENCE: int = 10
    
    def __post_init__(self):
        self.CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
        self.LOGS_DIR.mkdir(parents=True, exist_ok=True)

config = TrainingConfig()
