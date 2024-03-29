# Description: This file contains the code for the description of the data set.
#%%
# Imports
from statistics import mean

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils.preprocessing.transcript import *
#%% PACS data set description
# PACS folder path
PACS_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Data/PACS_data"

# load patient speech turns from all documents in folder
patient_turns = load_patient_turns_from_folder(folder_path=PACS_path)

# Different splits of patient turns
patient_chunks = split_into_chunks(patient_turns, chunk_size=150) # Split into chunks of 150 words
count_filtered = filter_by_word_count(patient_turns, min_word_count=150) # Filter out turns with less than 150 words

all_patient_turns = [item for sublist in patient_turns for item in sublist]

n_turns = 0
for lst in patient_turns:
    length = len(lst)
    n_turns += length

n_filtered = 0
for lst in count_filtered:
    length = len(lst)
    n_filtered += length

n_patient_chunks = 0
for lst in patient_chunks:
    length = len(lst)
    n_patient_chunks += length

avg_turn_length = average_word_count(patient_turns)

# Load and chunk (250+ words) all turns from all documents in folder
all_chunks = load_and_chunk_speech_turns(folder_path=PACS_path)

n_all_chunks = 0
for lst in all_chunks:
    length = len(lst)
    n_all_chunks += length

#%% Plot PACS results
# Bar plot of turns per document
turns_per_doc = [len(lst) for lst in patient_turns]
plt.figure(figsize=(10, 6))
sns.histplot(turns_per_doc, bins=20)
plt.xlabel('Turn Length')
plt.ylabel('Frequency')
plt.title('PACS Distribution of Patient Turns per Document')
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/PACS_Turns_per_document.png")

# Bar plot of patient turn length
plt.figure(figsize=(10, 6))
sns.histplot([len(turn.split()) for turn in all_patient_turns], bins=20, color="green")
plt.title("PACS Distribution of Patient Turn Length")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/PACS_Patient_turn_length.png")

#%% PACS training data description
# PACS folder path
PACS_train_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Data/PACS_train"

# load patient speech turns from all documents in folder
train_turns = load_patient_turns_from_folder(folder_path=PACS_train_path)

# Different splits of patient turns
patient_chunks = split_into_chunks(train_turns, chunk_size=150) # Split into chunks of 150 words
count_filtered = filter_by_word_count(train_turns, min_word_count=150) # Filter out turns with less than 150 words

all_train_turns = [item for sublist in train_turns for item in sublist]

n_train_turns = 0
for lst in train_turns:
    length = len(lst)
    n_train_turns += length

n_train_filtered = 0
for lst in count_filtered:
    length = len(lst)
    n_train_filtered += length

n_train_patient_chunks = 0
for lst in patient_chunks:
    length = len(lst)
    n_train_patient_chunks += length

avg_train_turn_length = average_word_count(train_turns)

# Load and chunk (250+ words) all turns from all documents in folder
all_chunks = load_and_chunk_speech_turns(folder_path=PACS_train_path)

n_all_chunks = 0
for lst in all_chunks:
    length = len(lst)
    n_all_chunks += length

#%% Plot PACS results
# Bar plot of turns per document
turns_per_doc = [len(lst) for lst in train_turns]
plt.figure(figsize=(10, 6))
sns.histplot(turns_per_doc, bins=20)
plt.xlabel('Turn Length')
plt.ylabel('Frequency')
plt.title('PACS_train Distribution of Patient Turns per Document')
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/PACS_train_Turns_per_document.png")

# Bar plot of patient turn length
plt.figure(figsize=(10, 6))
sns.histplot([len(turn.split()) for turn in all_train_turns], bins=20, color="mediumseagreen")
plt.title("PACS_train Distribution of Patient Turn Length")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/PACS_train_Patient_turn_length.png")

#%% PACS validation data description
# PACS folder path
PACS_val_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Data/PACS_val"

# load patient speech turns from all documents in folder
val_turns = load_patient_turns_from_folder(folder_path=PACS_val_path)

# Different splits of patient turns
patient_chunks = split_into_chunks(val_turns, chunk_size=150) # Split into chunks of 150 words
count_filtered = filter_by_word_count(val_turns, min_word_count=150) # Filter out turns with less than 150 words

all_val_turns = [item for sublist in val_turns for item in sublist]

n_val_turns = 0
for lst in val_turns:
    length = len(lst)
    n_val_turns += length

n_val_filtered = 0
for lst in count_filtered:
    length = len(lst)
    n_val_filtered += length

n_val_patient_chunks = 0
for lst in patient_chunks:
    length = len(lst)
    n_val_patient_chunks += length

avg_val_turn_length = average_word_count(val_turns)

# Load and chunk (250+ words) all turns from all documents in folder
all_chunks = load_and_chunk_speech_turns(folder_path=PACS_val_path)

n_all_chunks = 0
for lst in all_chunks:
    length = len(lst)
    n_all_chunks += length

#%% Plot PACS results
# Bar plot of turns per document
turns_per_doc = [len(lst) for lst in val_turns]
plt.figure(figsize=(10, 6))
sns.histplot(turns_per_doc, bins=20)
plt.xlabel('Turn Length')
plt.ylabel('Frequency')
plt.title('PACS_val Distribution of Patient Turns per Document')
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/PACS_val_Turns_per_document.png")

# Bar plot of patient turn length
plt.figure(figsize=(10, 6))
sns.histplot([len(turn.split()) for turn in all_val_turns], bins=20, color="lime")
plt.title("PACS_val Distribution of Patient Turn Length")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/PACS_val_Patient_turn_length.png")

#%% Anno-MI description
# Load anno-mi data
annomi = pd.read_csv("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Data/AnnoMI/AnnoMI-simple.csv")

# Clean text
timestamp = r'\b(\d{1,2}:[0-5][0-9]:[0-5][0-9])\b'
annomi['utterance_text'] = annomi['utterance_text'].str.replace(r'\[unintelligible ' + timestamp + r'\]', '<UNK>', regex=True)

# Filter out client turns
annomi_client = annomi[annomi['interlocutor'] == 'client']

annomi_client_turns = annomi_client['utterance_text'].tolist()
annomi_client_chunks = split_into_chunks(annomi_client_turns, chunk_size=150) # Split into chunks of 150 words
annomi_count_filtered = filter_by_word_count(annomi_client_turns, min_word_count=150) # Filter out turns with less than 150 words

#%% Plot Anno-MI results
# Bar plot of turn length
plt.figure(figsize=(10, 6))
sns.histplot([len(turn.split()) for turn in annomi_client_turns], bins=20, color="orange")
plt.title("Anno-MI Distribution of Client Turn Length")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/AnnoMI_Client_turn_length.png")

#%% DAIC-WOZ description
DAIC_WOZ_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Data/DAIC-WOZ/Transcripts"
daic_woz_files = os.listdir(DAIC_WOZ_path)

# Load patient speech turns from all documents in folder
daic_woz = pd.read_csv(os.path.join(DAIC_WOZ_path, daic_woz_files[0]))
for file in daic_woz_files[1:]:
    df = pd.read_csv(os.path.join(DAIC_WOZ_path, file))
    daic_woz = pd.concat([daic_woz, df])

# Different splits of patient turns
daic_woz_turns = daic_woz["Text"].tolist()
daic_woz_turns = [elem for elem in daic_woz_turns if isinstance(elem, str)]
utterance_lengths = [len(turn.split()) for turn in daic_woz_turns]

#%% HOPE description
# HOPE folder path
HOPE_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Data/HOPE"
hope_files = os.listdir(HOPE_path)


# Load patient speech turns from all documents in folder
hope = pd.read_csv(os.path.join(HOPE_path, hope_files[0]))
for file in hope_files[1:]:
    df = pd.read_csv(os.path.join(HOPE_path, file))
    hope = pd.concat([hope, df])

# Different splits of patient turns
hope_patient = hope[hope["Type"] == "P"]
hope_patient_turns = hope_patient["Utterance"].tolist()
hope_patient_turns = [elem for elem in hope_patient_turns if isinstance(elem, str)]
hope_patient_chunks = split_into_chunks(hope_patient_turns, chunk_size=150) # Split into chunks of 150 words
hope_count_filtered = filter_by_word_count(hope_patient_turns, min_word_count=150) # Filter out turns with less than 150 words

#%% Plot HOPE results
# Bar plot of turn length
plt.figure(figsize=(10, 6))

sns.histplot([len(turn.split()) for turn in hope_patient_turns], bins=20, color="steelblue")
plt.title("HOPE Distribution of Patient Turn Length")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/HOPE_Patient_turn_length.png")

#%% MEMO description
# MEMO folder path
MEMO_path = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Data/MEMO"
memo_files = os.listdir(MEMO_path)

# Load patient speech turns from all documents in folder
memo = pd.read_csv(os.path.join(MEMO_path, memo_files[0]))
for file in memo_files[1:]:
    df = pd.read_csv(os.path.join(MEMO_path, file))
    memo = pd.concat([memo, df])

# Different splits of patient turns
memo_patient = memo[memo["Type"] == "P"]
memo_patient_turns = memo_patient["Utterance"].tolist()
memo_patient_turns = [elem for elem in memo_patient_turns if isinstance(elem, str)]
memo_patient_chunks = split_into_chunks(memo_patient_turns, chunk_size=150) # Split into chunks of 150 words
memo_count_filtered = filter_by_word_count(memo_patient_turns, min_word_count=150) # Filter out turns with less than 150 words

#%% Plot MEMO results
# Bar plot of turn length
plt.figure(figsize=(10, 6))

sns.histplot([len(turn.split()) for turn in memo_patient_turns], bins=20, color="steelblue")
plt.title("MEMO Distribution of Patient Turn Length")
plt.xlabel("Word Count")
plt.ylabel("Frequency")
plt.savefig("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Figures/MEMO_Patient_turn_length.png")
#%%
# Print results
print("-------")
print("\n***PACS data set description***\n")
print(f"\nNumber of documents loaded: {len(patient_turns)}\n")
print(f"Number of patient turns: {n_turns}\n")
print(f"Average patient turns per document: {n_turns/len(patient_turns)}\n")
print(f"Average patient turn length: {avg_turn_length} words\n")
print(f"Number of patient turns with at least 150 words: {n_filtered}\n")
print(f"Number of arbitrary patient chunks with at least 150 words: {n_patient_chunks}\n")
print(f"Number of combined chunks with at least 250 words: {n_all_chunks}\n")
print("-------")

print("\n***HOPE data set description***\n")
print(f"\nNumber of documents loaded: {len(hope_files)}\n")
print(f"\nNumber of patient turns per document: {len(hope_patient)/len(hope_files)}\n")
print(f"\nNumber of patient turns: {len(hope_patient)}\n")
print(f"Number of patient chunks: {len(hope_patient_chunks)}\n")
print(f"Number of patient turns with at least 150 words: {len(hope_count_filtered)}\n")
print("-------")

print("\n***MEMO data set description***\n")
print(f"\nNumber of documents loaded: {len(memo_files)}\n")
print(f"\nNumber of patient turns per document: {len(memo_patient)/len(memo_files)}\n")
print(f"\nNumber of patient turns: {len(memo_patient)}\n")
print(f"Number of patient chunks: {len(memo_patient_chunks)}\n")
print(f"Number of patient turns with at least 150 words: {len(memo_count_filtered)}\n")
print("-------")

print("\n***Anno-MI data set description***\n")
print(f"\nNumber of client turns: {len(annomi_client_turns)}\n")
print(f"Number of client chunks: {len(annomi_client_chunks)}\n")
print(f"Number of client turns with at least 150 words: {len(annomi_count_filtered)}\n")

print("-------")

print("\n***DAIC-WOZ data set description***\n")
print(f"\nNumber of documents loaded: {len(daic_woz_files)}\n")
print(f"\nTotalt number of utterances: {len(daic_woz)}\n")
print(f"\nAverage number of utterances per document: {len(daic_woz)/len(daic_woz_files)}\n")
print(f"\nAverage length of utterances: {mean(utterance_lengths)}\n")
print("-------")

#%% Print to text file
with open("/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/Outputs/Descriptives/Dataset_descriptives.txt", 'w') as f:
    f.write("-------")
    f.write("\n***PACS data set description***\n")
    f.write(f"\nNumber of documents loaded: {len(patient_turns)}\n")
    f.write(f"Number of patient turns: {n_turns}\n")
    f.write(f"Average patient turns per document: {n_turns/len(patient_turns)}\n")
    f.write(f"Average patient turn length: {avg_turn_length} words\n")
    f.write(f"Number of patient turns with at least 150 words: {n_filtered}\n")
    f.write(f"Number of arbitrary patient chunks with at least 150 words: {n_patient_chunks}\n")
    f.write(f"Number of combined chunks with at least 250 words: {n_all_chunks}\n")
    f.write("-------")

    f.write("\n***HOPE data set description***\n")
    f.write(f"\nNumber of documents loaded: {len(hope_files)}\n")
    f.write(f"\nNumber of patient turns per document: {len(hope_patient)/len(hope_files)}\n")
    f.write(f"\nNumber of patient turns: {len(hope_patient)}\n")
    f.write(f"Number of patient chunks: {len(hope_patient_chunks)}\n")
    f.write(f"Number of patient turns with at least 150 words: {len(hope_count_filtered)}\n")
    f.write("-------")

    f.write("\n***MEMO data set description***\n")
    f.write(f"\nNumber of documents loaded: {len(memo_files)}\n")
    f.write(f"\nNumber of patient turns per document: {len(memo_patient)/len(memo_files)}\n")
    f.write(f"\nNumber of patient turns: {len(memo_patient)}\n")
    f.write(f"Number of patient chunks: {len(memo_patient_chunks)}\n")
    f.write(f"Number of patient turns with at least 150 words: {len(memo_count_filtered)}\n")
    f.write("-------")

    f.write("\n***Anno-MI data set description***\n")
    f.write(f"\nNumber of client turns: {len(annomi_client_turns)}\n")
    f.write(f"Number of client chunks: {len(annomi_client_chunks)}\n")
    f.write(f"Number of client turns with at least 150 words: {len(annomi_count_filtered)}\n")
    f.write("-------")

    f.write("\n***DAIC-WOZ data set description***\n")
    f.write(f"\nNumber of documents loaded: {len(daic_woz_files)}\n")
    f.write(f"\nTotalt number of utterances: {len(daic_woz)}\n")
    f.write(f"\nAverage number of utterances per document: {len(daic_woz)/len(daic_woz_files)}\n")
    f.write(f"\nAverage length of utterances: {mean(utterance_lengths)}\n")
    f.write("-------")