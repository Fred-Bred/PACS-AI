from sklearn.metrics import confusion_matrix, classification_report, accuracy_score, precision_score, recall_score
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sys
from collections import Counter

# Parse arguments
model_date = sys.argv[1] # Model date (e.g. 2024.03.13_11.54.44)
model_number = sys.argv[2] # Model number (e.g. 7)

# Define paths
output_folder = f"Outputs/trained_models/{model_date}"

# Define the classes
classes = ["Dismissing", "Secure", "Preoccupied"]

# Load predictions 
preds = pd.read_csv(f'{output_folder}/pacs.csv', sep='\t')
pred_labels = preds.iloc[:, 1].tolist()

# Load true labels
targets = pd.read_csv('Data/PACS_val.csv', sep='\t')
true_labels = targets.iloc[:, 1].tolist()

# Compute metrics
cm = confusion_matrix(true_labels, pred_labels)
cr = classification_report(true_labels, pred_labels, target_names=classes, zero_division=0)

accuracy = accuracy_score(true_labels, pred_labels)
precision = precision_score(true_labels, pred_labels, average='macro')
recall = recall_score(true_labels, pred_labels, average='macro')

# Print metrics
print(f'Accuracy: {accuracy}')
print(f'Precision: {precision}')
print(f'Recall: {recall}')
print('\nConfusion matrix:')
print(cm)
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
    f.write(f'Precision: {precision}\n')
    f.write(f'Recall: {recall}\n')
    f.write('\nConfusion matrix:\n')
    f.write(str(cm))
    f.write('\n\nClassification report:\n')
    f.write(str(cr))

# Add a new column to the dataframes representing the length of the instances
preds['length'] = preds.iloc[:, 0].apply(lambda x: len(x.split()))
targets['length'] = targets.iloc[:, 0].apply(lambda x: len(x.split()))

# Define a function to categorize the lengths into bins
def bin_length(length):
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

# Compute the metrics for each bin
for bin in sorted(grouped_preds.groups.keys(), key=sort_bins):
    pred_labels = grouped_preds.get_group(bin).iloc[:, 1].tolist()
    true_labels = grouped_targets.get_group(bin).iloc[:, 1].tolist()
    
    accuracy = accuracy_score(true_labels, pred_labels)
    
    bins.append(bin)
    accuracies.append(accuracy)

# Plot the results
plt.figure(figsize=(10, 10))
plt.plot(bins, accuracies, label='Accuracy')
plt.xlabel('Turn Length (words)')
plt.ylabel('Accuracy')
plt.title(f'Accuracy by Turn Length | Model {model_number} | {model_date}')
plt.savefig(f'{output_folder}/metrics_by_length_{model_date}_model {model_number}.png')

# Initialize a dictionary to store the class distributions for each bin
class_distributions = {}

# Compute the class distribution for each bin
for bin in sorted(grouped_targets.groups.keys()):
    true_labels = grouped_targets.get_group(bin).iloc[:, 1].tolist()
    class_distribution = Counter(true_labels)
    class_distributions[bin] = class_distribution

# Define a function to sort the bins
def sort_bins(bin):
    if bin == '751+':
        return 10000  # Return a large number for '751+' so it is sorted last
    return int(bin.split('-')[0])

# Sort the bins using the custom function
sorted_bins = sorted(class_distributions.keys(), key=sort_bins)

# # Plot the class distributions
# plt.figure(figsize=(10, 10))
# for class_label in sorted(list(class_distributions.values())[0].keys()):
#     plt.plot(sorted_bins, [class_distributions[bin][class_label] for bin in sorted_bins], label=f'Class {class_label}')
# plt.xlabel('Turn Length (words)')
# plt.ylabel('Number of Instances')
# plt.title(f'Class Distribution by Turn Length | Model {model_number} | {model_date}')
# plt.legend()
# plt.savefig(f'{output_folder}/class_distribution_by_length_{model_date}_model {model_number}.png')

# Plot the class distributions
plt.figure(figsize=(10, 10))

# Get the unique class labels
class_labels = sorted(list(class_distributions.values())[0].keys())

# Create a bar plot for each class
bar_width = 0.8 / len(class_labels)  # Adjust the bar width based on the number of classes
for i, class_label in enumerate(class_labels):
    plt.bar([j + i * bar_width for j in range(len(sorted_bins))],
            [class_distributions[bin][class_label] for bin in sorted_bins],
            width=bar_width,
            label=f'Class {class_label}')

# Set the x-ticks to be the bin names
plt.xticks(range(len(sorted_bins)), sorted_bins)

plt.xlabel('Turn Length (words)')
plt.ylabel('Number of Instances')
plt.title(f'Class Distribution by Turn Length (Validation Set)')
plt.legend()
plt.savefig(f'{output_folder}/class_distribution_by_length.png')