import torch
import torch.nn as nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
from torch.cuda.amp import GradScaler
from torch.utils.tensorboard import SummaryWriter
import os
import json

from training.config import config
from training.dataset import create_dataloaders
from training.model import create_dr_model
from training.train import train_one_epoch
from training.validate import validate

def main():
    print("Setting up training pipeline...")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # 1. DataLoaders
    # Note: Requires datasets to be present in config.DATA_DIR organized by class
    try:
        train_loader, val_loader, test_loader = create_dataloaders()
    except Exception as e:
        print(f"Failed to load datasets: {e}")
        print("Please ensure your dataset is placed in the 'datasets' folder structured as 0/, 1/, 2/, 3/, 4/")
        return
        
    # 2. Model
    model = create_dr_model(config.MODEL_NAME, config.NUM_CLASSES, config.PRETRAINED)
    model.to(device)
    
    # 3. Loss, Optimizer, Scheduler, Scaler
    # Use class weights if dataset is imbalanced (optional, here we use standard CE)
    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=config.LEARNING_RATE, weight_decay=config.WEIGHT_DECAY)
    scheduler = CosineAnnealingLR(optimizer, T_max=config.EPOCHS)
    scaler = GradScaler(enabled=config.MIXED_PRECISION)
    
    # 4. Logging
    writer = SummaryWriter(log_dir=str(config.LOGS_DIR))
    
    best_kappa = -1.0
    patience_counter = 0
    
    # 5. Training Loop
    for epoch in range(1, config.EPOCHS + 1):
        print(f"\n--- Epoch {epoch}/{config.EPOCHS} ---")
        
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, scaler, device, epoch, config)
        val_loss, val_metrics = validate(model, val_loader, criterion, device)
        
        scheduler.step()
        
        # Log to TensorBoard
        writer.add_scalar('Loss/Train', train_loss, epoch)
        writer.add_scalar('Accuracy/Train', train_acc, epoch)
        writer.add_scalar('Loss/Val', val_loss, epoch)
        writer.add_scalar('Accuracy/Val', val_metrics['accuracy'], epoch)
        writer.add_scalar('Kappa/Val', val_metrics['cohen_kappa'], epoch)
        
        print(f"Train Loss: {train_loss:.4f} | Acc: {train_acc:.2f}%")
        print(f"Val Loss: {val_loss:.4f} | Acc: {val_metrics['accuracy']*100:.2f}% | Kappa: {val_metrics['cohen_kappa']:.4f}")
        
        # 6. Early Stopping & Checkpointing
        current_kappa = val_metrics['cohen_kappa']
        if current_kappa > best_kappa:
            best_kappa = current_kappa
            patience_counter = 0
            
            # Save best model
            checkpoint_path = config.CHECKPOINT_DIR / "best_model.pth"
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'best_kappa': best_kappa,
                'metrics': val_metrics
            }, checkpoint_path)
            print(f"[*] Saved new best model with Kappa: {best_kappa:.4f}")
            
            # Save metrics to json
            with open(config.CHECKPOINT_DIR / "best_metrics.json", "w") as f:
                json.dump(val_metrics, f, indent=4)
        else:
            patience_counter += 1
            print(f"Early stopping patience: {patience_counter}/{config.PATIENCE}")
            if patience_counter >= config.PATIENCE:
                print("Early stopping triggered!")
                break
                
    writer.close()
    print("Training complete. Best model saved in checkpoints/best_model.pth")
    
if __name__ == "__main__":
    main()
