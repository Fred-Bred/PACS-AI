import os
import shutil
from sklearn.model_selection import train_test_split

# Paths
data_dir = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/PACS_data"
train_dir = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/PACS_train"
test_dir = "/home/unicph.domain/wqs493/ucph/securegroupdir/SAMF-SODAS-PACS/PACS_test"

# Create split
file_list = os.listdir(data_dir)
train_files, test_files = train_test_split(file_list, test_size=0.15, random_state=42)

# Copy files to respective directories
for file in train_files:
    shutil.copy2(os.path.join(data_dir, file), os.path.join(train_dir, file))
for file in test_files:
    shutil.copy2(os.path.join(data_dir, file), os.path.join(test_dir, file))