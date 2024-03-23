import os
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.utils import shuffle

import pandas as pd
from sklearn.utils import shuffle

def load_and_prepare_data(normal_traffic_path, botnet_files, excluded_file, random_state=42):
    """
    Loads and prepares the data by combining normal traffic data with malicious (botnet) traffic data,
    excluding one specific botnet file for training. Applies under-sampling on the malicious data to match
    the number of normal samples and over-samples the normal data by a factor of 4.
    """
    # Load normal traffic data with a label of 0
    df_normal = pd.read_csv(normal_traffic_path)
    df_normal['label'] = 0

    # Over-sample the normal data by a factor of 4
    df_normal_oversampled = df_normal.sample(n=df_normal.shape[0] * 4, replace=True, random_state=random_state)
    
    # Load and concatenate botnet traffic data, excluding the specified file, and label it with 1
    df_botnets = pd.concat([
        pd.read_csv(file) for file in botnet_files if file != excluded_file
    ])
    df_botnets['label'] = 1

    # Apply under-sampling on the malicious data to match the 25% of over-sampled number of normal samples for simulating natural situation
    df_botnets_sampled = df_botnets.sample(n=int(df_normal_oversampled.shape[0]/4), random_state=random_state)

    # Combine the over-sampled normal and sampled botnet datasets
    df_combined = pd.concat([df_normal_oversampled, df_botnets_sampled], ignore_index=True)
    df_combined = shuffle(df_combined, random_state=random_state)  # Shuffle to mix normal and malicious samples

    # Optional: Dropping specific columns, in this case some flag counts
    df_combined.drop(['fin_flag_cnt', 'syn_flag_cnt', 'rst_flag_cnt', 'ack_flag_cnt'], axis=1, inplace=True)

    return df_combined

from catboost import CatBoostRegressor
import os

def train_model_for_each_exclusion(normal_traffic_path, botnet_files_dir, models_dir, random_state=42):
    """
    Trains a CatBoost regressor for each combination of botnet files, excluding one at a time,
    and saves each model with a name indicating the excluded botnet scenario. Applies under-sampling
    on the malicious dataset to match the size of the normal dataset for each training iteration.
    Assumes that the label column for regression is continuous and represents a measure of anomaly or threat level.
    """
    # Filter for files that include 'botnet' in the filename and end with '_processed.csv'
    botnet_files = [
        os.path.join(botnet_files_dir, f) 
        for f in os.listdir(botnet_files_dir) 
        if 'botnet' in f and f.endswith('_processed.csv')
    ]

    for excluded_file in botnet_files:
        df_combined = load_and_prepare_data(normal_traffic_path, botnet_files, excluded_file, random_state=random_state)
        
        # Prepare the features (X) and labels (y)
        X = df_combined.drop('label', axis=1)
        y = df_combined['label']
        
        # Log the count of normal and malicious samples included in training
        print(f"Training with {excluded_file} excluded:")
        print(f"Normal samples: {df_combined[df_combined['label'] == 0].shape[0]}")
        print(f"Malicious samples: {df_combined[df_combined['label'] == 1].shape[0]} (after under-sampling)")
        
        # Train the CatBoost regressor
        model = CatBoostRegressor(verbose=0, random_state=random_state)
        model.fit(X, y)

        # Save the model, naming it to reflect the excluded botnet scenario but indicating it's a regressor model
        model_filename = os.path.basename(excluded_file).replace('_processed.csv', '_regressor_model.cbm')
        model.save_model(os.path.join(models_dir, model_filename))
        print(f"Model saved: {model_filename}\n")


if __name__ == "__main__":
    normal_traffic_path = "../../data/processed/CTU13_Normal_Traffic_80.csv"
    botnet_files_dir = "../../data/processed"
    models_dir = "../../models"
    
    # Ensure the models directory exists
    os.makedirs(models_dir, exist_ok=True)
    
    train_model_for_each_exclusion(normal_traffic_path, botnet_files_dir, models_dir)
