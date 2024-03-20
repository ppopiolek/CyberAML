import numpy as np


def calculate_size_statistics(flow_id, truncated_packets, direction=0):
    sizes = [
        pkt.size
        for pkt in truncated_packets
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction)
    ]

    if not sizes:
        return "No packets found matching criteria."

    size_mean = np.mean(sizes)
    size_min = np.min(sizes)
    size_max = np.max(sizes)
    size_std = np.std(sizes)

    return {"mean": size_mean, "min": size_min, "max": size_max, "std": size_std}


def calculate_delta_time_statistics(flow_id, truncated_packets, direction=0):
    import numpy as np

    timestamps = [
        pkt.timestamp
        for pkt in truncated_packets
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction)
    ]

    if len(timestamps) < 2:
        return "Insufficient packets for delta time calculation."

    # Sorting timestamps before calculating deltas to ensure chronological order
    timestamps = sorted(timestamps)
    # Calculating time deltas between consecutive packets
    delta_times = np.diff(timestamps)

    # Convert delta_times to a numpy array of type float to ensure compatibility with numpy operations
    delta_times = np.array(delta_times, dtype=float)

    delta_time_mean = np.mean(delta_times)
    delta_time_min = np.min(delta_times)
    delta_time_max = np.max(delta_times)
    delta_time_std = np.std(delta_times)

    return {
        "mean": delta_time_mean,
        "min": delta_time_min,
        "max": delta_time_max,
        "std": delta_time_std,
    }


def total_flow_size(flow_id, truncated_packets, direction=0):
    total_size = sum(
        pkt.size
        for pkt in truncated_packets
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction)
    )
    return total_size


def total_flow_duration(flow_id, truncated_packets, direction=0):
    timestamps = [
        pkt.timestamp
        for pkt in truncated_packets
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction)
    ]
    if timestamps:
        return max(timestamps) - min(timestamps)
    else:
        return "No packets found matching criteria."


def total_packet_count(flow_id, truncated_packets, direction=0):
    count = sum(
        1
        for pkt in truncated_packets
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction)
    )
    return count


def total_packet_count(flow_id, truncated_packets, direction=0):
    count = sum(
        1
        for pkt in truncated_packets
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction)
    )
    return count


def count_tcp_flags(flow_id, truncated_packets, direction=0):
    flags_count = {"FIN": 0, "SYN": 0, "RST": 0, "PSH": 0, "ACK": 0, "URG": 0}
    for pkt in truncated_packets:
        if (
            pkt.flow_id == flow_id
            and (direction == 0 or pkt.direction == direction)
            and pkt.tcp
        ):
            flags_count["FIN"] += pkt.fin
            flags_count["SYN"] += pkt.syn
            flags_count["RST"] += pkt.rst
            flags_count["PSH"] += pkt.psh
            flags_count["ACK"] += pkt.ack
            flags_count["URG"] += pkt.urg
    return flags_count
