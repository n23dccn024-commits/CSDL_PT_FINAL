class Peer:
    def __init__(self, peer_id):
        self.peer_id = peer_id
        self.local_storage = {}
        self.is_alive = True