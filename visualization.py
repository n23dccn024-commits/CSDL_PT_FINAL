import networkx as nx
import matplotlib.pyplot as plt
from pht import PHTNode

def draw_network_topology(dht, visited_prefixes):
    G = nx.DiGraph()
    labels = {}
    node_colors = []

    # 1. Nạp dữ liệu vào đồ thị (CHỈ ĐỌC TỪ CÁC NODE CÒN SỐNG)
    for peer in dht.node_list:
        if not peer.is_alive:
            continue
            
        for key, node in peer.local_storage.items():
            if isinstance(node, PHTNode):
                G.add_node(key)
                
                # Chỉ ghi tên máy chủ nếu node đó chưa có tên.
                if key not in labels:
                    labels[key] = f"[{node.min_val},{node.max_val}]\n({peer.peer_id})"
                
                if key != "root":
                    parent_key = key[:-1]
                    if parent_key == "": 
                        parent_key = "root"
                    G.add_edge(parent_key, key)

    for node in G.nodes():
        if node in visited_prefixes:
            node_colors.append('orange')
        else:
            node_colors.append('lightblue')

    # 2. THUẬT TOÁN CHỐNG ĐÈ NODE
    pos = {}
    
    def get_leaves_count(node_key):
        children = list(G.successors(node_key))
        if not children:
            return 1
        return sum(get_leaves_count(c) for c in children)

    def set_position(node_key, x_center, y, width):
        pos[node_key] = (x_center, y)
        children = list(G.successors(node_key))
        if children:
            children.sort()
            if len(children) == 1:
                set_position(children[0], x_center, y - 2.0, width)
            else:
                left_child, right_child = children[0], children[1]
                left_leaves = get_leaves_count(left_child)
                right_leaves = get_leaves_count(right_child)
                total_leaves = left_leaves + right_leaves
                
                left_width = width * (left_leaves / total_leaves)
                right_width = width * (right_leaves / total_leaves)
                
                left_x = x_center - (width / 2) + (left_width / 2)
                right_x = x_center + (width / 2) - (right_width / 2)
                
                padding = width * 0.05
                set_position(left_child, left_x, y - 2.0, left_width - padding)
                set_position(right_child, right_x, y - 2.0, right_width - padding)

    if "root" in G.nodes():
        set_position("root", x_center=0, y=0, width=100)

    for node in G.nodes():
        if node not in pos:
            pos[node] = (0, 0)

    # 3. Render đồ thị
    plt.figure(figsize=(16, 9))
    
    nx.draw(G, pos, node_color=node_colors, with_labels=False, 
            node_size=1200, edge_color='gray', arrows=True, arrowsize=15)
    
    nx.draw_networkx_labels(G, pos, labels, font_size=7, font_weight='bold')
    
    plt.title("Prefix Hash Tree - Physical & Logical Mapping", fontsize=16, fontweight='bold')
    plt.axis('off')
    
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        plt.tight_layout()
        
    plt.show()