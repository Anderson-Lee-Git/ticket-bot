import os
import pandas as pd
from sklearn.model_selection import train_test_split


# A function that summarizes the dataframe by the total number of samples
def summarize(df):
    print(df.shape[0])


# Define the path to the data directory
data_dir = './data'

# Get a list of all .png files in the data directory
image_files = [f for f in os.listdir(data_dir) if f.endswith('.png')]

# Create a dataframe with the image_id column
df = pd.DataFrame({'image_id': [os.path.splitext(f)[0] for f in image_files]})

# Split the dataframe into train, val, and test sets
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.3333, random_state=42)  # 0.3333 * 0.3 ≈ 0.1

# Summarize each df
train_summary = summarize(train_df)
val_summary = summarize(val_df)
test_summary = summarize(test_df)

# Define the path to the meta directory
meta_dir = './meta'

# Save the dataframes to the meta directory
train_df.to_csv(os.path.join(meta_dir, 'train.csv'), index=False)
val_df.to_csv(os.path.join(meta_dir, 'val.csv'), index=False)
test_df.to_csv(os.path.join(meta_dir, 'test.csv'), index=False)
