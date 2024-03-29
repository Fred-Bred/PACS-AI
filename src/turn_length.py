# Imports
import sys

import pandas as pd

from utils.preprocessing.transcript import load_data_with_labels

# Arguments
target_length = sys.argv[1] # Target length of the instances

# Load data
pacs_train = load_data_with_labels("Data/PACS_labels.xlsx", "Data/PACS_train")
pacs_dev = load_data_with_labels("Data/PACS_labels.xlsx", "Data/PACS_val")
pacs_test = load_data_with_labels("Data/PACS_labels.xlsx", "Data/PACS_test")

# Combine turns within documents to reach the target length
def combine_turns(data, target_length):
    combined_data = pd.DataFrame(columns=["text", "label", "document"])
    current_length = 0
    current_document = ""
    current_turn = ""
    current_label = ""
    for index, row in data.iterrows():
        turn_length = len(row["text"].split())
        if current_length + turn_length < target_length and (current_document == row["document"] or current_document == ""):
            current_document = row["document"]
            current_turn += row["text"] + " "
            current_label = row["label"]
            current_length += turn_length
        else:
            if current_length >= target_length:  # Add this line
                new_row = pd.DataFrame({"text": [current_turn], "label": [current_label], "document": [current_document]})
                combined_data = pd.concat([combined_data, new_row], ignore_index=True)
            current_length = turn_length
            current_document = row["document"]
            current_turn = row["text"] + " "
            current_label = row["label"]
    combined_data.reset_index(drop=True, inplace=True)
    return combined_data

# Combine and clean train turns
pacs_train_combined = combine_turns(pacs_train, int(target_length))
# Remove tabs and newlines from text
pacs_train_combined['text'] = pacs_train_combined['text'].str.replace(r'\t', ' ', regex=True)
pacs_train_combined['text'] = pacs_train_combined['text'].str.replace(r'\n', ' ', regex=True)

# Combine and clean dev and test turns
pacs_dev_combined = combine_turns(pacs_dev, int(target_length))

# Remove tabs and newlines from text
pacs_dev_combined['text'] = pacs_dev_combined['text'].str.replace(r'\t', ' ', regex=True)
pacs_dev_combined['text'] = pacs_dev_combined['text'].str.replace(r'\n', ' ', regex=True)

# Combine and clean test turns
pacs_test_combined = combine_turns(pacs_test, int(target_length))
# Remove tabs and newlines from text
pacs_test_combined['text'] = pacs_test_combined['text'].str.replace(r'\t', ' ', regex=True)
pacs_test_combined['text'] = pacs_test_combined['text'].str.replace(r'\n', ' ', regex=True)

# Save the combined data
pacs_train_combined.to_csv(f"Data/PACS_varying_lengths/train_length_{target_length}.csv", index=False, sep="\t")
pacs_dev_combined.to_csv(f"Data/PACS_varying_lengths/val_length_{target_length}.csv", index=False, sep="\t")
pacs_test_combined.to_csv(f"Data/PACS_varying_lengths/test_length_{target_length}.csv", index=False, sep="\t")
