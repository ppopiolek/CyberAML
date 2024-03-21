import pandas as pd

def preprocess_traffic(filepath):
    """
    Preprocesses traffic data by keeping selected columns and removing missing values.

    Parameters:
    - filepath: Path to the input CSV file.
    
    Returns:
    - df_clean: A cleaned pandas DataFrame.
    """
    # Predefined list of columns to keep
    columns_to_keep = [
        "tot_fwd_pkts", "tot_bwd_pkts", "totlen_fwd_pkts", "totlen_bwd_pkts",
        "fwd_pkt_len_max", "fwd_pkt_len_min", "fwd_pkt_len_mean", "fwd_pkt_len_std",
        "bwd_pkt_len_max", "bwd_pkt_len_min", "bwd_pkt_len_mean", "bwd_pkt_len_std",
        "pkt_len_mean", "pkt_len_std",
        "flow_iat_mean", "flow_iat_max", "flow_iat_min", "flow_iat_std",
        "fwd_iat_tot", "fwd_iat_max", "fwd_iat_min", "fwd_iat_mean", "fwd_iat_std",
        "bwd_iat_tot", "bwd_iat_max", "bwd_iat_min", "bwd_iat_mean", "bwd_iat_std",
        "fin_flag_cnt", "syn_flag_cnt", "rst_flag_cnt", 
        "ack_flag_cnt"
    ]

    # Load the dataset
    df = pd.read_csv(filepath)

    # Keep only the desired columns
    df_filtered = df[columns_to_keep]

    # Drop rows with any missing values
    df_clean = df_filtered.dropna()

    return df_clean

def main():
    input_path = "../../data/external/CTU13_Normal_Traffic.csv"
    output_path = "../../data/interim/CTU13_Normal_Traffic_preprocessed.csv"
    
    # Preprocess the data and return the cleaned DataFrame
    df_clean = preprocess_traffic(input_path)
    
    # Save the cleaned DataFrame to a new CSV file when called directly
    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned normal data saved to {output_path}")
    
    
    input_path = "../../data/external/CTU13_Attack_Traffic.csv"
    output_path = "../../data/processed/CTU13_attack_all_scenarios.csv"
    
    # Preprocess the data and return the cleaned DataFrame
    df_clean = preprocess_traffic(input_path)
    
    # Save the cleaned DataFrame to a new CSV file when called directly
    df_clean.to_csv(output_path, index=False)
    print(f"Cleaned attack data saved to {output_path}")

if __name__ == "__main__":
    main()
