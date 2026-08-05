import torch
from tqdm import tqdm
from torch.cuda.amp import autocast

def train_one_epoch(model, dataloader, criterion, optimizer, scaler, device, epoch, config):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    pbar = tqdm(dataloader, desc=f"Epoch {epoch} Training")
    for inputs, labels in pbar:
        inputs, labels = inputs.to(device), labels.to(device)
        
        optimizer.zero_grad()
        
        # Mixed precision training
        with autocast(enabled=config.MIXED_PRECISION):
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
        if config.MIXED_PRECISION:
            scaler.scale(loss).backward()
            if config.GRADIENT_CLIPPING > 0:
                scaler.unscale_(optimizer)
                torch.nn.utils.clip_grad_norm_(model.parameters(), config.GRADIENT_CLIPPING)
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            if config.GRADIENT_CLIPPING > 0:
                torch.nn.utils.clip_grad_norm_(model.parameters(), config.GRADIENT_CLIPPING)
            optimizer.step()
            
        running_loss += loss.item() * inputs.size(0)
        
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
        
        pbar.set_postfix({'loss': loss.item(), 'acc': 100. * correct / total})
        
    epoch_loss = running_loss / len(dataloader.dataset)
    epoch_acc = 100. * correct / total
    
    return epoch_loss, epoch_acc
