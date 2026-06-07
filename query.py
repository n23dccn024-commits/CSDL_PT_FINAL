def standard_dht_query(dht, q_min, q_max):
    results = []
    for val in range(q_min, q_max + 1):
        key = f"exact_{val}"
        data = dht.get(key)
        if data:
            results.extend(data)
    return results