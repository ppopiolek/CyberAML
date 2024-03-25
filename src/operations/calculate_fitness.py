from src.utils.flow import *
from src.utils.flow_calculations import *
from src.utils.restoration import *
from src.utils.truncated_packet import *
from src.operations.size_perturbation_logic import *
from src.operations.timing_perturbation_logic import *
import pandas as pd
import joblib
import catboost

def prepare_size_stats(truncated_packets, flow_id):
    
    size_stats = calculate_size_statistics(flow_id, truncated_packets, direction=0)
    size_stats_fwd = calculate_size_statistics(flow_id, truncated_packets, direction=1)
    size_stats_bwd = calculate_size_statistics(flow_id, truncated_packets, direction=2)
    
    total_fwd_pkts = total_packet_count(flow_id, truncated_packets, direction=1)
    total_bwd_pkts = total_packet_count(flow_id, truncated_packets, direction=2)
    
    totlen_fwd_pkts = total_flow_size(flow_id, truncated_packets, direction=1)
    totlen_bwd_pkts = total_flow_size(flow_id, truncated_packets, direction=2)
    
    

    adjusted_size_stats = {
        "tot_fwd_pkts": total_fwd_pkts,
        "tot_bwd_pkts": total_bwd_pkts,
        "totlen_fwd_pkts": totlen_fwd_pkts,
        "totlen_bwd_pkts": totlen_bwd_pkts,
        "fwd_pkt_len_max": size_stats_fwd['max'],
        "fwd_pkt_len_min": size_stats_fwd['min'],
        "fwd_pkt_len_mean": size_stats_fwd['mean'],
        "fwd_pkt_len_std": size_stats_fwd['std'],
        "bwd_pkt_len_max": size_stats_bwd['max'],
        "bwd_pkt_len_min": size_stats_bwd['min'],
        "bwd_pkt_len_mean": size_stats_bwd['mean'],
        "bwd_pkt_len_std": size_stats_bwd['std'],
        "pkt_len_mean": size_stats['mean'],
        "pkt_len_std": size_stats['std'],
    }
    
    

    return adjusted_size_stats


def prepare_timing_stats(truncated_packets, flow_id):
    """
    Obtain and adjust timing statistics for a specific flow ID from truncated packets,
    considering the entire flow as well as forward and backward directions separately.
    """
    # Obtain timing stats for the entire flow (direction=0)
    timing_stats_total = calculate_delta_time_statistics(flow_id, truncated_packets, direction=0)
    # Obtain timing stats for the forward direction (fwd, direction=1)
    timing_stats_fwd = calculate_delta_time_statistics(flow_id, truncated_packets, direction=1)
    # Obtain timing stats for the backward direction (bwd, direction=2)
    timing_stats_bwd = calculate_delta_time_statistics(flow_id, truncated_packets, direction=2)

    # Combining and adjusting timing stats to the expected format for MAD calculation
    adjusted_timing_stats = {
        "flow_iat_mean": timing_stats_total.get('mean', 0),
        "flow_iat_max": timing_stats_total.get('max', 0),
        "flow_iat_min": timing_stats_total.get('min', 0),
        "flow_iat_std": timing_stats_total.get('std', 0),
        "fwd_iat_tot": timing_stats_fwd.get('total', 0),
        "fwd_iat_max": timing_stats_fwd.get('max', 0),
        "fwd_iat_min": timing_stats_fwd.get('min', 0),
        "fwd_iat_mean": timing_stats_fwd.get('mean', 0),
        "fwd_iat_std": timing_stats_fwd.get('std', 0),
        "bwd_iat_tot": timing_stats_bwd.get('total', 0),
        "bwd_iat_max": timing_stats_bwd.get('max', 0),
        "bwd_iat_min": timing_stats_bwd.get('min', 0),
        "bwd_iat_mean": timing_stats_bwd.get('mean', 0),
        "bwd_iat_std": timing_stats_bwd.get('std', 0),
    }

    return adjusted_timing_stats


def predict_single_flow(model_name, sizing_stats, timing_stats):

    flow_stats = {**sizing_stats, **timing_stats}
    
    flow_df = pd.DataFrame([flow_stats])

    models_folder = '../models/fitness' # from notebook
    #models_folder = '../models' # TODO: TEST - from notebook
    #models_folder = '../../models/fitness' # oryg.?
    clf = joblib.load(f"{models_folder}/{model_name}_RF_model.pkl") # oryg.
    #from catboost import CatBoostClassifier, CatBoostRegressor
    #model = CatBoostRegressor()
    #model.load_model(f"{models_folder}/botnet-capture-20110815-fast-flux-2_regressor_model.cbm")
    probabilities = clf.predict_proba(flow_df) # oryg.
    #probabilities = model.predict(flow_df)
    
    malicious_probability = probabilities[0][1]
    #malicious_probability = probabilities
    
    #print(f"Malicious score (probability) for the flow: {malicious_probability*100:.2f}%")
    
    return malicious_probability


def predict_single_flow_target(model_name, sizing_stats, timing_stats):

    flow_stats = {**sizing_stats, **timing_stats}
    
    flow_df = pd.DataFrame([flow_stats])

    #models_folder = '../models/fitness' # from notebook
    models_folder = '../models' # TODO: TEST - from notebook
    #models_folder = '../../models/fitness' # oryg.?
    #clf = joblib.load(f"{models_folder}/{model_name}_RF_model.pkl") # oryg.
    from catboost import CatBoostClassifier, CatBoostRegressor
    model = CatBoostRegressor()
    model.load_model(f"{models_folder}/{model_name}_regressor_model.cbm")
    #probabilities = clf.predict_proba(flow_df) # oryg.
    probabilities = model.predict(flow_df)
    
    #malicious_probability = probabilities[0][1]
    malicious_probability = probabilities[0]
    
    #print(f"Malicious score (probability) for the flow: {malicious_probability*100:.2f}%")
    
    return malicious_probability