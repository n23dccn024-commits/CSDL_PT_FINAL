import pandas as pd
import sys
from dht import DHT_Network
from pht import PrefixHashTree
from query import standard_dht_query
from visualization import draw_network_topology

def run_normal_scenario():
    print("==================================================")
    print("KHOI DONG HE THONG MANG P2P (NORMAL SCENARIO)")
    print("==================================================")
    network = DHT_Network()
    pht = PrefixHashTree(network, global_min=-20, global_max=50)

    file_path = "dataset/iot_telemetry_data.csv"
    try:
        df = pd.read_csv(file_path)
        records_list = df.to_dict('records')
        print(f"[OK] Da nap {len(records_list)} ban ghi cam bien thuc te.")
    except FileNotFoundError:
        print(f"[LOI] Khong tim thay file '{file_path}'. Chay 'fetch_data.py' truoc!")
        sys.exit()

    print("[OK] Dang phan phoi du lieu vao mang (Insert)...")
    for record in records_list:
        pht.insert(record)
        temp = record['temperature']
        exact_key = f"exact_{temp}"
        existing = network.get(exact_key)
        if existing:
            existing.append(record)
            network.put(exact_key, existing)
        else:
            network.put(exact_key, [record])

    print("\n--- 1. THUC THI RANGE QUERY: DAI HEP (NARROW: 25C den 26C) ---")
    network.reset_metrics()
    standard_dht_query(network, 25, 26)
    dht_narrow_msg = network.message_count
    
    network.reset_metrics()
    pht.parallel_range_query("root", 25, 26, [], [])
    pht_narrow_msg = network.message_count
    
    print(f"-> Standard DHT Message Overhead: {dht_narrow_msg} messages")
    print(f"-> PHT Range Query Message Overhead: {pht_narrow_msg} messages")
    print(f"   (Nhan xet: Voi dai hep, PHT ton chi phi duyet cay nen Message Overhead gan tuong duong DHT)")

    print("\n--- 2. THUC THI RANGE QUERY: DAI RONG (WIDE: 20C den 30C) ---")
    network.reset_metrics()
    standard_dht_query(network, 20, 30)
    dht_wide_msg = network.message_count
    
    network.reset_metrics()
    results_pht = []
    visited_prefixes = []
    pht.parallel_range_query("root", 20, 30, results_pht, visited_prefixes)
    pht_wide_msg = network.message_count
    
    print(f"-> Standard DHT Message Overhead: {dht_wide_msg} messages")
    print(f"-> PHT Range Query Message Overhead: {pht_wide_msg} messages")
    print(f"   (Nhan xet: Voi dai rong, PHT the hien suc manh vuot troi nho co che Cat Tia (Pruning)!)")

    print(f"\n[THANH CONG] Gom duoc {len(results_pht)} ban ghi thoa man trong dai rong.")
    
    print("\n[OK] Dang render do thi NetworkX Topology cho Dai Rong (20C - 30C)...")
    draw_network_topology(network, visited_prefixes)

if __name__ == "__main__":
    run_normal_scenario()