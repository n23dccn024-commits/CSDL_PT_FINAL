class PHTNode:
    def __init__(self, prefix, min_val, max_val):
        self.prefix = prefix
        self.min_val = min_val
        self.max_val = max_val
        self.records = []

class PrefixHashTree:
    def __init__(self, dht, global_min=-20, global_max=50, max_items=50):
        self.dht = dht
        self.global_min = global_min
        self.global_max = global_max
        self.max_items = max_items
        root = PHTNode("root", global_min, global_max)
        self.dht.put("root", root)

    def insert(self, record):
        temp_val = record['temperature']
        if temp_val < self.global_min or temp_val > self.global_max:
            return

        current_prefix = "root"
        node = self.dht.get(current_prefix)
        if not node: return

        while True:
            left_prefix = current_prefix + "0"
            right_prefix = current_prefix + "1"
            left_child = self.dht.get(left_prefix)
            right_child = self.dht.get(right_prefix)

            if not left_child and not right_child:
                if len(node.records) < self.max_items or (node.max_val - node.min_val <= 1):
                    node.records.append(record)
                    self.dht.put(current_prefix, node)
                    return
                else:
                    mid = (node.min_val + node.max_val) // 2
                    left_node = PHTNode(left_prefix, node.min_val, mid)
                    right_node = PHTNode(right_prefix, mid + 1, node.max_val)

                    for r in node.records:
                        if r['temperature'] <= mid:
                            left_node.records.append(r)
                        else:
                            right_node.records.append(r)
                    node.records = []

                    self.dht.put(current_prefix, node)
                    self.dht.put(left_prefix, left_node)
                    self.dht.put(right_prefix, right_node)

                    left_child = left_node
                    right_child = right_node

            mid = (node.min_val + node.max_val) // 2
            if temp_val <= mid:
                current_prefix = left_prefix
                node = left_child
            else:
                current_prefix = right_prefix
                node = right_child

    def parallel_range_query(self, current_prefix, q_min, q_max, results, visited_prefixes):
        node = self.dht.get(current_prefix)
        if not node: return

        visited_prefixes.append(current_prefix)

        if node.max_val < q_min or node.min_val > q_max:
            return

        left_prefix = current_prefix + "0"
        right_prefix = current_prefix + "1"

        left_child = self.dht.get(left_prefix)
        right_child = self.dht.get(right_prefix)

        if not left_child and not right_child:
            for r in node.records:
                if q_min <= r['temperature'] <= q_max:
                    results.append(r)
            return

        self.parallel_range_query(left_prefix, q_min, q_max, results, visited_prefixes)
        self.parallel_range_query(right_prefix, q_min, q_max, results, visited_prefixes)