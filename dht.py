import hashlib
from peer import Peer

class DHT_Network:
    def __init__(self):
        peer_labels = ["Node_A", "Node_B", "Node_C", "Node_D", "Node_E"]
        self.nodes = {label: Peer(label) for label in peer_labels}
        self.node_list = list(self.nodes.values())
        self.message_count = 0

    def _get_primary_and_replica(self, key):
        # Dùng thuật toán SHA-256 chuẩn công nghiệp để băm dữ liệu cố định
        hash_val = int(hashlib.sha256(key.encode('utf-8')).hexdigest(), 16)
        idx1 = hash_val % len(self.node_list)
        idx2 = (idx1 + 1) % len(self.node_list)
        return self.node_list[idx1], self.node_list[idx2]

    def put(self, key, value):
        primary, replica = self._get_primary_and_replica(key)
        primary.local_storage[key] = value
        replica.local_storage[key] = value

    def get(self, key):
        self.message_count += 1
        primary, replica = self._get_primary_and_replica(key)

        if primary.is_alive:
            return primary.local_storage.get(key, None)
        else:
            print(f"[SYSTEM ALERT] {primary.peer_id} is OFFLINE (Timeout for key: {key}).")
            print(f"               --> Rerouting query to Replica ({replica.peer_id})...")
            self.message_count += 1
            if replica.is_alive:
                return replica.local_storage.get(key, None)
            return None

    def reset_metrics(self):
        self.message_count = 0

    def kill_node(self, peer_id):
        if peer_id in self.nodes:
            self.nodes[peer_id].is_alive = False
            print(f"\n[CRITICAL EVENT] {peer_id} has been KILLED (Disconnected)!\n")