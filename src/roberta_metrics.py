import os
import datetime

from torchmetrics import Accuracy, Precision, Recall, ConfusionMatrix
import torch
from torch.utils.data import DataLoader, Subset
import matplotlib.pyplot as plt
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import numpy as np
from tqdm import tqdm
from sklearn.metrics import confusion_matrix, classification_report

from utils.trainer import Trainer
from utils.preprocessing.transcript import load_data_with_labels
from utils.dataset import CustomDataset

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_id = "roberta-base"
model_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/trained_models/unspecified_checkpoint_EPOCH_2_SAMPLES_5629_BATCHSIZE_16.pt"

classes = ["Dismissing", "Secure", "Preoccupied"]
num_labels = len(classes)

id2label = {i: label for i, label in enumerate(classes)}
label2id = {label: i for i, label in enumerate(classes)}

# Instantiate the tokenizer and the model
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForSequenceClassification.from_pretrained(
    model_id,
    num_labels=num_labels,
    id2label=id2label,
    label2id=label2id)
model.to(device)

# Data folder
train_data_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/PACS_train"
labels_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/PACS_labels.xlsx"

# Load data
data = load_data_with_labels(labels_path, train_data_path)
data["label"] = data["label"].astype(int) - 1 # Convert labels to 0, 1, 2

max_len = 512
dataset = CustomDataset(data, max_len=max_len, tokenizer=tokenizer)

# Create a list of indices from 0 to the length of the dataset
indices = list(range(len(dataset)))

# Shuffle the indices
np.random.shuffle(indices, random_state=42)

# Create a train and validation subset of variable dataset with torch
train_size = int(0.89 * len(dataset))
val_size = len(dataset) - train_size

# Split the indices into train and validation sets
train_indices = indices[:train_size]
val_indices = indices[train_size:]

# Use the Subset class for the train and validation subsets
train_dataset = Subset(dataset, train_indices)
val_dataset = Subset(dataset, val_indices)

# Put train dataset into a loader with 2 batches and put test data in val loader
batch_size = 16
train_loader = DataLoader(train_dataset, batch_size=batch_size)
val_loader = DataLoader(val_dataset, batch_size=batch_size)

# Instantiate the Trainer
trainer = Trainer()
# trainer.compile(model, torch.optim.AdamW, learning_rate=5e-5, loss_fn=torch.nn.CrossEntropyLoss())
trainer.model = model
trainer.val_loader = val_loader

# Load the saved weights into the model
model_state_dict = torch.load(model_path)
model.load_state_dict(model_state_dict)

# Initialize the metrics
accuracy = Accuracy(task="multiclass", average=None, num_classes=num_labels)
precision = Precision(task='multiclass', average=None, num_classes=num_labels)
recall = Recall(task='multiclass', average=None, num_classes=num_labels)

# Make sure to switch the model to evaluation mode
trainer.model.eval()

# Initialize lists to store the true and predicted labels
true_labels = []
pred_labels = []

with torch.no_grad():
    # Create a progress bar
    progress_bar = tqdm(val_loader, desc="Validation", total=len(val_loader))

    for batch in progress_bar:
        inputs = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)
        labels = batch['targets'].to(device)

        # Get the model's predictions
        outputs = trainer.model(inputs, attention_mask=attention_mask)
        _, preds = torch.max(outputs.logits, 1)

        # Update the metrics
        accuracy.update(preds, labels)
        precision.update(preds, labels)
        recall.update(preds, labels)

        # Store the true and predicted labels
        true_labels.extend(labels.cpu().numpy())
        pred_labels.extend(preds.cpu().numpy())

        # Update the progress bar
        progress_bar.set_postfix({'accuracy': accuracy.compute().tolist(), 'precision': precision.compute().tolist(), 'recall': recall.compute().tolist()})
       
# Compute the confusion matrix
cm = confusion_matrix(true_labels, pred_labels)
print("\nConfusion matrix:")
print(cm)

# Compute the final metrics
print("\nFinal metrics:")
final_accuracy = accuracy.compute()
final_precision = precision.compute()
final_recall = recall.compute()

print(f"Accuracy: {final_accuracy}")
print(f"Precision: {final_precision}")
print(f"Recall: {final_recall}")

# Print the classification report
print("\nClassification report:")
print(classification_report(true_labels, pred_labels, target_names=classes))