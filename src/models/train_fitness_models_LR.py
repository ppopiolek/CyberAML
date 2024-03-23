import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib

def load_and_train(folder_path, normal_data_path, models_save_path):
    normal_data = pd.read_csv(normal_data_path)
    normal_data['label'] = 0

    for filename in os.listdir(folder_path):
        if 'botnet' in filename and filename.endswith('_processed.csv'):
            malicious_data = pd.read_csv(os.path.join(folder_path, filename))
            malicious_data['label'] = 1

            combined_data = pd.concat([normal_data, malicious_data], ignore_index=True)
            combined_data.drop(['fin_flag_cnt', 'syn_flag_cnt', 'rst_flag_cnt', 'ack_flag_cnt'], axis=1, inplace=True)  # Omit flag counts for now
            
            X = combined_data.drop('label', axis=1)
            y = combined_data['label']
            
            # Skalowanie cech
            #scaler = StandardScaler()
            #X_scaled = scaler.fit_transform(X)
            
            clf = LogisticRegression(random_state=42, max_iter=5000)
            clf.fit(X, y)
            
            model_name = filename.replace('_processed.csv', '_LR_model.pkl')
            joblib.dump(clf, os.path.join(models_save_path, model_name))
            
            print(f'Trained: {model_name}')


if __name__ == '__main__':
    processed = '../../data/processed'
    normal = '../../data/processed/CTU13_Normal_Traffic_20.csv'
    save = '../../models/fitness'

    load_and_train(processed, normal, save)
