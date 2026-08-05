import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, cohen_kappa_score,
    matthews_corrcoef, roc_auc_score, roc_curve
)
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class EvaluationMetrics:
    def __init__(self, output_dir="results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.classes = [0, 1, 2, 3, 4]
        self.class_names = ["No DR", "Mild", "Moderate", "Severe", "Proliferative"]

    def compute_all_metrics(self, y_true, y_pred, y_prob):
        """
        Computes comprehensive evaluation metrics and saves reports.
        y_true: 1D array of true labels
        y_pred: 1D array of predicted labels
        y_prob: 2D array of predicted probabilities (N_samples, N_classes)
        """
        metrics = {}
        
        # Basic metrics
        metrics['accuracy'] = accuracy_score(y_true, y_pred)
        metrics['precision_macro'] = precision_score(y_true, y_pred, average='macro', zero_division=0)
        metrics['recall_macro'] = recall_score(y_true, y_pred, average='macro', zero_division=0)
        metrics['f1_macro'] = f1_score(y_true, y_pred, average='macro', zero_division=0)
        
        # Advanced metrics
        metrics['cohen_kappa'] = cohen_kappa_score(y_true, y_pred, weights='quadratic')
        metrics['mcc'] = matthews_corrcoef(y_true, y_pred)
        
        # ROC AUC (One-vs-Rest)
        try:
            metrics['roc_auc_ovr'] = roc_auc_score(y_true, y_prob, multi_class='ovr')
        except ValueError:
            metrics['roc_auc_ovr'] = float('nan') # In case a class is entirely missing in the batch

        # Specificity and Sensitivity per class
        cm = confusion_matrix(y_true, y_pred, labels=self.classes)
        specificity = []
        sensitivity = []
        for i in range(len(self.classes)):
            tp = cm[i, i]
            fn = np.sum(cm[i, :]) - tp
            fp = np.sum(cm[:, i]) - tp
            tn = np.sum(cm) - (tp + fn + fp)
            
            spec = tn / (tn + fp) if (tn + fp) > 0 else 0
            sens = tp / (tp + fn) if (tp + fn) > 0 else 0
            specificity.append(spec)
            sensitivity.append(sens)
            
        metrics['specificity_macro'] = np.mean(specificity)
        metrics['sensitivity_macro'] = np.mean(sensitivity)
        
        # Generate Reports
        self.save_classification_report(y_true, y_pred)
        self.plot_confusion_matrix(cm)
        self.plot_roc_curve(y_true, y_prob)
        
        # Save metrics to CSV
        metrics_df = pd.DataFrame([metrics])
        metrics_df.to_csv(self.output_dir / "evaluation_metrics.csv", index=False)
        
        return metrics
        
    def save_classification_report(self, y_true, y_pred):
        report = classification_report(y_true, y_pred, target_names=self.class_names, output_dict=True, zero_division=0)
        df = pd.DataFrame(report).transpose()
        df.to_csv(self.output_dir / "classification_report.csv")
        
    def plot_confusion_matrix(self, cm):
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=self.class_names, yticklabels=self.class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig(self.output_dir / "confusion_matrix.png", dpi=300)
        plt.close()
        
    def plot_roc_curve(self, y_true, y_prob):
        plt.figure(figsize=(8, 6))
        for i in range(len(self.classes)):
            # Create binary labels for the current class
            y_true_binary = (np.array(y_true) == i).astype(int)
            if np.sum(y_true_binary) == 0:
                continue # Skip if class not present in ground truth
                
            fpr, tpr, _ = roc_curve(y_true_binary, np.array(y_prob)[:, i])
            auc = roc_auc_score(y_true_binary, np.array(y_prob)[:, i])
            plt.plot(fpr, tpr, label=f'{self.class_names[i]} (AUC = {auc:.2f})')
            
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curve (One-vs-Rest)')
        plt.legend(loc="lower right")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / "roc_curve.png", dpi=300)
        plt.close()
