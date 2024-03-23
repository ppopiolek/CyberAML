import numpy as np


def calculate_size_statistics(flow_id, truncated_packets, direction=0):
    """
    Calculates size statistics (mean, min, max, std) for packets in a specified flow_id and direction,
    taking into account packet fragmentation.
    
    Parameters:
    - flow_id: The specific flow_id for which to calculate size statistics.
    - truncated_packets: A list of TruncatedPacket objects.
    - direction: The direction of packets to include (0 for all, 1 for src->dst (fwd), 2 for dst->src (bwd)).
    
    Returns:
    A dictionary with calculated size statistics: mean, min, max, std or a message if no packets match criteria.
    """
    sizes = []
    for pkt in truncated_packets:
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction):
            if pkt.fragmented == 0:
                sizes.append(pkt.size)
            elif pkt.fragmented == 1:
                sizes.extend([pkt.size / 2, pkt.size / 2])  # Fragment into 2 parts
            elif pkt.fragmented == 2:
                sizes.extend([pkt.size / 4] * 4)  # Fragment into 4 parts

    if not sizes:
        return {
        "mean": 0.0,
        "min": 0.0,
        "max": 0.0,
        "std": 0.0,
    }

    size_mean = np.mean(sizes) 
    size_min = np.min(sizes)
    size_max = np.max(sizes)
    size_std = np.std(sizes)

    return {"mean": size_mean, "min": size_min, "max": size_max, "std": size_std}



def calculate_delta_time_statistics(flow_id, truncated_packets, direction=0):
  # Prepare a list of timestamps, taking packet fragmentation into account
    timestamps = []
    for pkt in truncated_packets:
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction):
            # Duplicate the timestamp for fragmented packets according to their fragmentation level
            if pkt.fragmented == 0:
                timestamps.append(pkt.timestamp)
            elif pkt.fragmented == 1:
                # Duplicate the timestamp for 2-way fragmentation
                timestamps.extend([pkt.timestamp, pkt.timestamp])
            elif pkt.fragmented == 2:
                # Duplicate the timestamp for 4-way fragmentation
                timestamps.extend([pkt.timestamp] * 4)

    if len(timestamps) < 2:
        return {
        "mean": 0.0,
        "min": 0.0,
        "max": 0.0,
        "std": 0.0,
    }

    # Sort timestamps before calculating deltas to ensure chronological order
    timestamps = sorted(timestamps)
    # Calculate time deltas between consecutive timestamps
    delta_times = np.diff(timestamps)

    # Convert delta_times to a numpy array of float type to ensure compatibility with numpy operations
    delta_times = np.array(delta_times, dtype=float)

    # Calculate and return statistical measures for delta times
    delta_time_mean = np.mean(delta_times) * 1000000.0
    delta_time_min = np.min(delta_times) * 1000000.0
    delta_time_max = np.max(delta_times) * 1000000.0
    delta_time_std = np.std(delta_times) * 1000000.0

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
        return (max(timestamps) - min(timestamps)) * 1000000.0
    else:
        return 0.0


def total_packet_count(flow_id, truncated_packets, direction=0):
    """
    Counts the total number of packets for a specified flow_id and direction,
    taking into account packet fragmentation.
    
    Parameters:
    - flow_id: The specific flow_id to count packets for.
    - truncated_packets: A list of TruncatedPacket objects.
    - direction: The direction of packets to include (0 for all, 1 for src->dst, 2 for dst->src).
    
    Returns:
    The total packet count, including individual fragments as separate packets.
    """
    count = sum(
        # Count each packet normally if not fragmented
        1 if pkt.fragmented == 0 else
        # Count as 2 packets if fragmented into 2 parts
        2 if pkt.fragmented == 1 else
        # Count as 4 packets if fragmented into 4 parts
        4
        for pkt in truncated_packets
        if pkt.flow_id == flow_id and (direction == 0 or pkt.direction == direction)
    )
    return count


# TODO: czy tu sie uwzglednia fragmentacje 
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
