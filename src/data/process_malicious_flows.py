import os
import pandas as pd
from cic_preprocess import preprocess_traffic

def process_and_save_files(source_dir, dest_dir):
    """
    Processes files containing 'botnet' in their name in the source directory using
    the preprocess_traffic function, then saves them to the destination directory with
    '_processed.csv' appended to their original filename.

    :param source_dir: Path to the source directory.
    :param dest_dir: Path to the destination directory.
    """
    # Ensure pandas is available
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("This script requires pandas. Please install it using 'pip install pandas'.")

    for filename in os.listdir(source_dir):
        if 'botnet' in filename and filename.endswith('_flow.csv'):
            source_file_path = os.path.join(source_dir, filename)
            dest_file_path = os.path.join(dest_dir, filename.replace('_flow.csv', '_processed.csv'))
            
            print(f"Processing {source_file_path}...")

            # Process the file
            df_clean = preprocess_traffic(source_file_path)
            
            # Save the processed DataFrame to a new CSV file
            df_clean.to_csv(dest_file_path, index=False)
            
            print(f"Saved processed data to {dest_file_path}")

if __name__ == "__main__":
    source_dir = "../../data/interim"
    dest_dir = "../../data/processed"

    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    process_and_save_files(source_dir, dest_dir)

