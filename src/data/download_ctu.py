import os
import requests
import pandas as pd
import numpy as np

MAPPING = {
    'src_ip': None,
    'dst_ip': None,
    'src_port': None,
    'dst_port': None,
    'protocol': None,
    'timestamp': None,
    'flow_duration': 'Flow Duration',
    'flow_byts_s': 'Flow Byts/s',
    'flow_pkts_s': 'Flow Pkts/s',
    'fwd_pkts_s': None,
    'bwd_pkts_s': None,
    'tot_fwd_pkts': 'Tot Fwd Pkts',
    'tot_bwd_pkts': 'Tot Bwd Pkts',
    'totlen_fwd_pkts': 'TotLen Fwd Pkts',
    'totlen_bwd_pkts': 'TotLen Bwd Pkts',
    'fwd_pkt_len_max': 'Fwd Pkt Len Max',
    'fwd_pkt_len_min': 'Fwd Pkt Len Min',
    'fwd_pkt_len_mean': 'Fwd Pkt Len Mean',
    'fwd_pkt_len_std': 'Fwd Pkt Len Std',
    'bwd_pkt_len_max': 'Bwd Pkt Len Max',
    'bwd_pkt_len_min': 'Bwd Pkt Len Min',
    'bwd_pkt_len_mean': 'Bwd Pkt Len Mean',
    'bwd_pkt_len_std': 'Bwd Pkt Len Std',
    'pkt_len_max': None,
    'pkt_len_min': None,
    'pkt_len_mean': 'Pkt Len Mean',
    'pkt_len_std': 'Pkt Len Std',
    'pkt_len_var': 'Pkt Len Var',
    'fwd_header_len': 'Fwd Header Len',
    'bwd_header_len': 'Bwd Header Len',
    'fwd_seg_size_min': None,
    'fwd_act_data_pkts': None,
    'flow_iat_mean': 'Flow IAT Mean',
    'flow_iat_max': 'Flow IAT Max',
    'flow_iat_min': 'Flow IAT Min',
    'flow_iat_std': 'Flow IAT Std',
    'fwd_iat_tot': 'Fwd IAT Tot',
    'fwd_iat_max': 'Fwd IAT Max',
    'fwd_iat_min': 'Fwd IAT Min',
    'fwd_iat_mean': 'Fwd IAT Mean',
    'fwd_iat_std': 'Fwd IAT Std',
    'bwd_iat_tot': 'Bwd IAT Tot',
    'bwd_iat_max': 'Bwd IAT Max',
    'bwd_iat_min': 'Bwd IAT Min',
    'bwd_iat_mean': 'Bwd IAT Mean',
    'bwd_iat_std': 'Bwd IAT Std',
    'fwd_psh_flags': 'Fwd PSH Flags',
    'bwd_psh_flags': 'Bwd PSH Flags',
    'fwd_urg_flags': None,
    'bwd_urg_flags': None,
    'fin_flag_cnt': 'FIN Flag Cnt',
    'syn_flag_cnt': 'SYN Flag Cnt',
    'rst_flag_cnt': 'RST Flag Cnt',
    'psh_flag_cnt': None,
    'ack_flag_cnt': 'ACK Flag Cnt',
    'urg_flag_cnt': None,
    'ece_flag_cnt': None,
    'down_up_ratio': 'Down/Up Ratio',
    'pkt_size_avg': 'Pkt Size Avg',
    'init_fwd_win_byts': None,
    'init_bwd_win_byts': 'Init Bwd Win Byts',
    'active_max': 'Active Max',
    'active_min': 'Active Min',
    'active_mean': 'Active Mean',
    'active_std': 'Active Std',
    'idle_max': 'Idle Max',
    'idle_min': 'Idle Min',
    'idle_mean': 'Idle Mean',
    'idle_std': 'Idle Std',
    'fwd_byts_b_avg': None,
    'fwd_pkts_b_avg': None,
    'bwd_byts_b_avg': None,
    'bwd_pkts_b_avg': None,
    'fwd_blk_rate_avg': None,
    'bwd_blk_rate_avg': None,
    'fwd_seg_size_avg': 'Fwd Seg Size Avg',
    'bwd_seg_size_avg': 'Bwd Seg Size Avg',
    'cwr_flag_count': None,
    'subflow_fwd_pkts': None,
    'subflow_bwd_pkts': None,
    'subflow_fwd_byts': None,
    'subflow_bwd_byts': None
}

def download_csv(url, save_path):
    """
    Download a CSV file from a specified URL and save it to a given path.
    
    Parameters:
    - url: URL of the CSV file to download.
    - save_path: Path where the CSV file will be saved.
    """
    response = requests.get(url)
    response.raise_for_status()  

    with open(save_path, 'wb') as file:
        file.write(response.content)

if __name__ == "__main__":
    # URL of the CSV file on GitHub
    csv1_url = "https://github.com/imfaisalmalik/CTU13-CSV-Dataset/blob/main/CTU13_Normal_Traffic.csv?raw=true"
    csv2_url = "https://github.com/imfaisalmalik/CTU13-CSV-Dataset/blob/main/CTU13_Attack_Traffic.csv?raw=true"
    save_path1 = "../../data/external/CTU13_Normal_Traffic.csv" 
    save_path2 = "../../data/external/CTU13_Attack_Traffic.csv" 
    os.makedirs(os.path.dirname(save_path1), exist_ok=True)
    download_csv(csv1_url, save_path1)
    os.makedirs(os.path.dirname(save_path2), exist_ok=True)
    download_csv(csv2_url, save_path2)
    
    # Load the downloaded CSV file
    df1 = pd.read_csv(save_path1)
    df2 = pd.read_csv(save_path2)
    
    # Rename columns based on MAPPING and drop columns not in MAPPING
    df1 = df1.rename(columns={v: k for k, v in MAPPING.items() if v in df1.columns})
    df1 = df1.reindex(columns=MAPPING.keys())  # Reorder according to MAPPING keys
    df1.to_csv(save_path1, index=False)
    
    df2 = df2.rename(columns={v: k for k, v in MAPPING.items() if v in df2.columns})
    df2 = df2.reindex(columns=MAPPING.keys())  # Reorder according to MAPPING keys
    df2.to_csv(save_path2, index=False)
    
    print(f"CSV files downloaded, processed, and saved to {save_path1}, and {save_path2}")
