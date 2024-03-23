import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
import joblib
import pandas as pd

def load_and_train(folder_path, normal_data_path, models_save_path):

    normal_data = pd.read_csv(normal_data_path)
    normal_data['label'] = 0  

    for filename in os.listdir(folder_path):
        if 'botnet' in filename and filename.endswith('_processed.csv'):

            malicious_data = pd.read_csv(os.path.join(folder_path, filename))
            malicious_data['label'] = 1 

            combined_data = pd.concat([normal_data, malicious_data], ignore_index=True)
            
            combined_data.drop(['fin_flag_cnt', 'syn_flag_cnt', 'rst_flag_cnt', 'ack_flag_cnt'], axis=1, inplace=True) # for now ommit flag
            
            X = combined_data.drop('label', axis=1)
            y = combined_data['label']
            
            
            clf = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=3)
            clf.fit(X, y)
            
            model_name = filename.replace('_processed.csv', '_RF_model.pkl')
            joblib.dump(clf, os.path.join(models_save_path, model_name))
            
            chosen_tree = clf.estimators_[0]  
            #plt.figure(figsize=(20, 10))
            #plot_tree(chosen_tree, filled=True, feature_names=list(X.columns), class_names=['Normal', 'Attack'], max_depth=3)
            #plt.title("Example Tree from Random Forest")
            #plt.show()
            print(f'trained: {model_name}')


if __name__ == '__main__':
    processed = '../../data/processed'
    normal = '../../data/processed/CTU13_Normal_Traffic_20.csv'
    save = '../../models/fitness'

    load_and_train(processed, normal, save)


