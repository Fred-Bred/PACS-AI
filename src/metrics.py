from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import argparse
from collections import Counter
import os

# Parse arguments
parser = argparse.ArgumentParser(description="Compute metrics for a model")
parser.add_argument("--model_date", type=str, help="Model date (e.g. 2024.03.13_11.54.44)")
parser.add_argument("--model_number", type=int, help="Model number (e.g. 7)")
parser.add_argument("--model_name", type=str, help="Model name (e.g. roberta-base)")
parser.add_argument("--min_length", type=int, help="Minimum length of the instances (0 for single pt turns)")
parser.add_argument("--mode", type=str, help="Mode (val or test)", default="val")
parser.add_argument("--split", type=str, help="Whether to use the new (stratified) or the old (random) split", default="new")

args = parser.parse_args()

model_date = args.model_date # Model date (e.g. 2024.03.13_11.54.44)
model_number = args.model_number # Model number (e.g. 7)
model_name = args.model_name # Model name (e.g. roberta-base)
min_length = args.min_length # Minimum length of the instances (0 for single pt turns)
mode = args.mode # Mode (val or test)
split = args.split # Whether to use the new (stratified) or the old (random) split

# Define paths
output_folder = f"Outputs/trained_models/{model_date}"
os.makedirs(output_folder, exist_ok=True)

# Define the classes
classes = ["Dismissing", "Secure", "Preoccupied"]

# Load predictions 
preds = pd.read_csv(f'{output_folder}/pacs.csv', sep='\t')
pred_labels = preds.iloc[:, 1].tolist()

# Load true labels
if split == "old":
    targets = pd.read_csv('Data/old_PACS/PACS_val.csv', sep='\t') if min_length == 0 else pd.read_csv(f'Data/PACS_varying_lengths/val_length_{min_length}.csv', sep='\t')
elif split == "new":
    if mode == "test":
        targets = pd.read_csv('Data/test_PACS.csv', sep='\t') if min_length == 0 else pd.read_csv(f'Data/PACS_varying_lengths/test_combined_{min_length}.csv', sep='\t')
    elif mode == "val":
        targets = pd.read_csv('Data/val_PACS.csv', sep='\t') if min_length == 0 else pd.read_csv(f'Data/PACS_varying_lengths/val_combined_{min_length}.csv', sep='\t')
    else:
        raise ValueError("Invalid mode argument. Must be 'val' or 'test'.")
else:
    raise ValueError("Invalid split argument. Must be 'old' or 'new'.")
true_labels = targets.iloc[:, 1].tolist()

# Compute metrics
cm = confusion_matrix(true_labels, pred_labels, labels=[1, 2, 3])
cr = classification_report(true_labels, pred_labels, target_names=classes, zero_division=0)

accuracy = accuracy_score(true_labels, pred_labels)
recall = recall_score(true_labels, pred_labels, average='macro', zero_division=0)
precision = precision_score(true_labels, pred_labels, average='macro', zero_division=0)
f1 = f1_score(true_labels, pred_labels, average='macro', zero_division=0)

# Compute normalised confusion matrix
cm_norm = confusion_matrix(true_labels, pred_labels, labels=[1, 2, 3], normalize='true')
cm_norm = np.round(cm_norm, 2)

# Print metrics
print(f'Accuracy: {accuracy}')
print('\nConfusion matrix:')
print(cm)
print('\nNormalised confusion matrix:')
print(cm_norm)
print('\nClassification report:')
print(cr)

# Plot and save the confusion matrix
plt.figure(figsize=(10, 10))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title(f'Confusion Matrix | Model {model_number} | {model_date}')
plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, rotation=45)
plt.yticks(tick_marks, classes)
plt.xlabel('Predicted label')
plt.ylabel('True label')
plt.savefig(f'{output_folder}/confusion_matrix_{model_date}.png')

# Write metrics to text file
with open(f'{output_folder}/metrics_model_{model_number}.txt', 'w') as f:
    f.write('\n\nValidation metrics:\n')
    f.write(f'Accuracy: {accuracy}\n')
    f.write('\nConfusion matrix:\n')
    f.write(str(cm))
    f.write('\n\nNormalised confusion matrix:\n')
    f.write(str(cm_norm))
    f.write('\n\nClassification report:\n')
    f.write(str(cr))

# Add a new column to the dataframes representing the length of the instances
preds['length'] = preds.iloc[:, 0].apply(lambda x: len(x.split()))
targets['length'] = targets.iloc[:, 0].apply(lambda x: len(x.split()))

# Define a function to categorize the lengths into bins
def bin_length(length):
    if min_length == 100:
        if length <= 150:
            return '100-150'
        elif length <= 200:
            return '151-200'
        elif length <= 300:
            return '201-300'
        elif length <= 400:
            return '301-400'
        elif length <= 500:
            return '401-500'
        elif length <= 750:
            return '501-750'
        else:
            return '751+'
    elif min_length == 50:
        if length <= 100:
            return '50-100'
        elif length <= 150:
            return '101-150'
        elif length <= 200:
            return '151-200'
        elif length <= 300:
            return '201-300'
        elif length <= 400:
            return '301-400'
        elif length <= 500:
            return '401-500'
        elif length <= 750:
            return '501-750'
        else:
            return '751+'
    else:
        if length <= 5:
            return '0-5'
        elif length <= 50:
            return '6-50'
        elif length <= 100:
            return '51-100'
        elif length <= 150:
            return '101-150'
        elif length <= 200:
            return '151-200'
        elif length <= 300:
            return '201-300'
        elif length <= 400:
            return '301-400'
        elif length <= 500:
            return '401-500'
        elif length <= 750:
            return '501-750'
        else:
            return '751+'

# Apply the function to the 'length' column to create a new 'bin' column
preds['bin'] = preds['length'].apply(bin_length)
targets['bin'] = targets['length'].apply(bin_length)

# Group the data by 'bin'
grouped_preds = preds.groupby('bin')
grouped_targets = targets.groupby('bin')

# Define a function to sort the bins
def sort_bins(bin):
    if bin == '751+':
        return 10000  # Return a large number for '751+' so it is sorted last
    return int(bin.split('-')[1]) if '-' in bin else int(bin.split('+')[0])

# Initialize lists to store the metrics for each bin
bins = []
accuracies = []
recalls = []
precisions = []
f1s = []

# Compute the metrics for each bin and also count the class distribution
# class_counts = []
for bin in sorted(grouped_preds.groups.keys(), key=sort_bins):
    pred_labels = grouped_preds.get_group(bin).iloc[:, 1].tolist()
    true_labels = grouped_targets.get_group(bin).iloc[:, 1].tolist()
    
    accuracy = accuracy_score(true_labels, pred_labels)
    recall = recall_score(true_labels, pred_labels, average='macro', zero_division=0)
    precision = precision_score(true_labels, pred_labels, average='macro', zero_division=0)
    f1 = f1_score(true_labels, pred_labels, average='macro', zero_division=0)
        
    # # Count the class distribution
    # class_count = np.bincount(true_labels)
    # class_counts.append(class_count)
    
    bins.append(bin)
    accuracies.append(accuracy)
    recalls.append(recall)
    precisions.append(precision)
    f1s.append(f1)

# Plot the results
fig, ax1 = plt.subplots(figsize=(10, 10))

# Plot histogram
counts = [len(grouped_preds.get_group(bin)) for bin in bins]
ax1.bar(bins, counts, color='gray', alpha=0.5, label='Number of Samples')

# Plot the line graph
ax2 = ax1.twinx()
ax2.plot(bins, accuracies, label='Accuracy', color='b')

# Set labels and title
ax1.set_xlabel('Turn Length (words)')
ax1.set_ylabel('Number of Samples', color='gray')
ax2.set_ylabel('Accuracy', color='b')

if min_length == 0:
    plt.title(f'Accuracy by Turn Length | Single PT Turns | Mode: {mode}')
else:
    plt.title(f'Accuracy by Turn Length | Min Input Length: {min_length} Words')

# Set legend
fig.legend(loc="upper right")

plt.savefig(f'{output_folder}/accuracy_by_length_{model_date}_model_{model_number}_{mode}.png')

# New plot with all metrics
fig, ax1 = plt.subplots(figsize=(10, 10))

# Plot histogram
counts = [len(grouped_preds.get_group(bin)) for bin in bins]
ax1.bar(bins, counts, color='gray', alpha=0.5, label='Number of Samples')

# Plot the line graphs
ax2 = ax1.twinx()
ax2.plot(bins, accuracies, label='Accuracy', color='b')
ax2.plot(bins, recalls, label='Recall', color='g')
ax2.plot(bins, precisions, label='Precision', color='r')
ax2.plot(bins, f1s, label='F1', color='c')

# Set labels and title
ax1.set_xlabel('Turn Length (words)')
ax1.set_ylabel('Number of Samples', color='gray')
ax2.set_ylabel('Metric', color='b')

if min_length == 0:
    plt.title(f'Metrics by Turn Length | {model_name} | Single PT Turns | Mode: {mode}')
else:
    plt.title(f'Metrics by Turn Length | {model_name} | Min Input Length: {min_length} Words')

# Set legend
fig.legend(loc="upper right")

plt.savefig(f'{output_folder}/metrics_by_length_{model_date}_model_{model_number}_{mode}.png')

# # Plot with stacked bars instead of histogram

# # Plot the results
# fig, ax1 = plt.subplots(figsize=(10, 10))

# # Plot the stacked bar chart for class distribution
# # Ensure all inner lists in class_counts have the same length
# max_len = max(len(lst) for lst in class_counts)
# class_counts = [lst + [None]*(max_len-len(lst)) for lst in class_counts]
# class_counts = np.array(class_counts).T
# ax1.bar(bins, class_counts[0], color='gray', alpha=0.5, label='Class 0')
# for i in range(1, class_counts.shape[0]):
#     ax1.bar(bins, class_counts[i], bottom=np.sum(class_counts[:i], axis=0), alpha=0.5, label=f'Class {i}')

# # Plot the line graph for accuracy
# ax2 = ax1.twinx()
# ax2.plot(bins, accuracies, label='Accuracy', color='b')

# # Set labels and title
# ax1.set_xlabel('Turn Length (words)')
# ax1.set_ylabel('Number of Samples', color='gray')
# ax2.set_ylabel('Metric', color='b')

# if min_length == 0:
#     plt.title(f'Accuracy by Turn Length | {model_name} | Single PT Turns | Mode: {mode}')
# else:
#     plt.title(f'Accuracy by Turn Length | {model_name} | Min Input Length: {min_length} Words')

# # Set legend
# fig.legend(loc="upper right")

# plt.savefig(f'{output_folder}/accuracy_by_length_wclasses_{model_date}_model_{model_number}_{mode}.png')

# # Initialize a dictionary to store the class distributions for each bin
# class_distributions = {}

# # Compute the class distribution for each bin
# for bin in sorted(grouped_targets.groups.keys()):
#     true_labels = grouped_targets.get_group(bin).iloc[:, 1].tolist()
#     class_distribution = Counter(true_labels)
#     class_distributions[bin] = class_distribution

# # Define a function to sort the bins
# def sort_bins(bin):
#     if bin == '751+':
#         return 10000  # Return a large number for '751+' so it is sorted last
#     return int(bin.split('-')[0])

# # Sort the bins using the custom function
# sorted_bins = sorted(class_distributions.keys(), key=sort_bins)

# # Plot the class distributions
# plt.figure(figsize=(10, 10))

# # Get the unique class labels
# class_labels = sorted(list(class_distributions.values())[0].keys())

# # Create a bar plot for each class
# bar_width = 0.8 / len(class_labels)  # Adjust the bar width based on the number of classes
# for i, class_label in enumerate(class_labels):
#     plt.bar([j + i * bar_width for j in range(len(sorted_bins))],
#             [class_distributions[bin][class_label] for bin in sorted_bins],
#             width=bar_width,
#             label=f'Class {class_label}')

# # Set the x-ticks to be the bin names
# plt.xticks(range(len(sorted_bins)), sorted_bins)

# plt.xlabel('Turn Length (words)')
# plt.ylabel('Number of Instances')
# plt.title(f'Class Distribution by Turn Length (Validation Set)')
# plt.legend()
# plt.savefig(f'{output_folder}/class_distribution_by_length.png')