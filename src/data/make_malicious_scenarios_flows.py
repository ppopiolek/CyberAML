import os
import subprocess

def convert_pcap_to_csv(source_file, dest_file):
    """
    Converts a pcap or pcapng file to csv using cicflowmeter.

    :param source_file: Path to the source pcap or pcapng file.
    :param dest_file: Path to the destination csv file.
    """
    cmd = ['cicflowmeter', '-f', source_file, '-c', dest_file]
    subprocess.run(cmd, check=True)

def process_directory(source_dir, dest_dir):
    """
    Processes all pcap or pcapng files in the given source directory, converting them
    to csv format in the destination directory with '_flow.csv' appended to the original filename.

    :param source_dir: Path to the source directory containing pcap or pcapng files.
    :param dest_dir: Path to the destination directory for the csv files.
    """
    for filename in os.listdir(source_dir):
        if filename.endswith(('.pcap', '.pcapng')):
            source_file = os.path.join(source_dir, filename)
            dest_filename = f"{os.path.splitext(filename)[0]}_flow.csv"
            dest_file = os.path.join(dest_dir, dest_filename)
            convert_pcap_to_csv(source_file, dest_file)
            print(f"Processed {source_file} to {dest_file}")

if __name__ == "__main__":
    source_dir = "../../data/raw"
    dest_dir = "../../data/interim"

    # Create destination directory if it doesn't exist
    os.makedirs(dest_dir, exist_ok=True)

    process_directory(source_dir, dest_dir)

