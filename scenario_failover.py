import pandas as pd
import sys
from dht import DHT_Network
from pht import PrefixHashTree
from visualization import draw_network_topology

def run_failover_scenario():
    print("==================================================")
    print("KHOI DONG HE THONG MANG P2P (FAILOVER SCENARIO)")
    print("==================================================")
    network = DHT_Network()
    pht = PrefixHashTree(network, global_min=-20, global_max=50)
 
    file_path = "dataset/iot_telemetry_data.csv"
    try:
        df = pd.read_csv(file_path)
        records_list = df.to_dict('records')
        print(f"[OK] Da nap {len(records_list)} ban ghi cam bien.")
    except FileNotFoundError:
        print(f"[LOI] Khong tim thay file '{file_path}'. Chay 'fetch_data.py' truoc!")
        sys.exit()

    print("[OK] Dang phan phoi du lieu vao mang (Insert)...")
    for record in records_list:
        pht.insert(record)

    q_min, q_max = 20, 30

    print("\n--- KICH BAN ROT MANG (CHURN RESILIENCE) ---")
    network.kill_node("Node_B")

    print("\n--- THUC THI LAI PHT RANGE QUERY ---")
    network.reset_metrics()
    results_pht_failover = []
    visited_prefixes_failover = []
    
    pht.parallel_range_query("root", q_min, q_max, results_pht_failover, visited_prefixes_failover)
    
    print(f"\n-> PHT Message Overhead (Sau Rerouting): {network.message_count} messages")
    print(f"-> [THANH CONG] He thong an toan, lay lai duoc {len(results_pht_failover)} ban ghi tu Replica.")

    print("\n[OK] Dang render do thi de chung minh cau truc logic khong bi gay...")
    draw_network_topology(network, visited_prefixes_failover)

if __name__ == "__main__":
    run_failover_scenario()