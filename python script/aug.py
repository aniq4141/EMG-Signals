import pandas as pd
import imgaug.augmenters as iaa
import numpy as np

# Load the dataset
df = pd.read_csv("down.csv")

# Convert columns to numeric data type
df["AnalogValue"] = pd.to_numeric(df["AnalogValue"])
df["Density"] = pd.to_numeric(df["Density"])
df["Amplitude"] = pd.to_numeric(df["Amplitude"])

# Define augmentation techniques
augmenter = iaa.Sequential([
    iaa.AdditiveGaussianNoise(scale=(0, 0.1*255)),  # Gaussian noise augmentation
    iaa.Multiply((0.8, 1.2))  # Scaling augmentation
])

# Apply data augmentation
augmented_data = []
for index, row in df.iterrows():
    augmented_sample = row.copy()
    augmented_sample["AnalogValue"] = augmenter.augment_image(np.array([[row["AnalogValue"]]], dtype=np.float32))[0, 0]
    augmented_sample["Density"] = augmenter.augment_image(np.array([[row["Density"]]], dtype=np.float32))[0, 0]
    augmented_sample["Amplitude"] = augmenter.augment_image(np.array([[row["Amplitude"]]], dtype=np.float32))[0, 0]
    augmented_data.append(augmented_sample)

# Combine augmented data with original dataset
augmented_df = pd.concat([df] + augmented_data, ignore_index=True)

# Save the augmented dataset
augmented_df.to_csv("down_augmented_dataset.csv", index=False)
