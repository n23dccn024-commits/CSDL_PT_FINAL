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

    print("\n--- THUC THI RANGE QUERY (Muc tieu: 20C den 30C) ---")
    q_min, q_max = 20, 30

    network.reset_metrics()
    standard_dht_query(network, q_min, q_max)
    print(f"-> Standard DHT Message Overhead: {network.message_count} messages")

    network.reset_metrics()
    results_pht = []
    visited_prefixes = []
    pht.parallel_range_query("root", q_min, q_max, results_pht, visited_prefixes)
    print(f"-> PHT Range Query Message Overhead: {network.message_count} messages")

    print(f"\n[THANH CONG] Gom duoc {len(results_pht)} ban ghi thoa man.")
    
    print("\n[OK] Dang render do thi NetworkX Topology...")
    draw_network_topology(network, visited_prefixes)

if __name__ == "__main__":
    run_normal_scenario()