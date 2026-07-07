import torch
import torch.nn.functional as F
from tqdm import tqdm
from .metrics import EvaluationMetrics

@torch.no_grad()
def validate(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    
    all_preds = []
    all_labels = []
    all_probs = []
    
    pbar = tqdm(dataloader, desc="Validation")
    for inputs, labels in pbar:
        inputs, labels = inputs.to(device), labels.to(device)
        
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        
        running_loss += loss.item() * inputs.size(0)
        
        probs = F.softmax(outputs, dim=1)
        _, preds = torch.max(outputs, 1)
        
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        all_probs.extend(probs.cpu().numpy())
        
        pbar.set_postfix({'loss': loss.item()})
        
    epoch_loss = running_loss / len(dataloader.dataset)
    
    evaluator = EvaluationMetrics(output_dir="results/val")
    metrics = evaluator.compute_all_metrics(all_labels, all_preds, all_probs)
    
    return epoch_loss, metrics
