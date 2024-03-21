from sklearn.model_selection import train_test_split
import pandas as pd

# Load your preprocessed dataset
df = pd.read_csv("../../data/interim/CTU13_Normal_Traffic_preprocessed.csv" )

# Split the dataset into training and testing sets with an 80/20 ratio
# Set a specific random state (seed) for reproducibility
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Save the training and testing sets to new CSV files
train_df.to_csv("../../data/processed/CTU13_Normal_Traffic_80.csv" , index=False)
test_df.to_csv("../../data/processed/CTU13_Normal_Traffic_20.csv" , index=False)

