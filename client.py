"""2D R-Tree Spatial Indexing Engine.
100% Python Standard Library.
"""

class SimpleRTree:
    """Spatial index over 2D bounding boxes [min_x, min_y, max_x, max_y]."""
    def __init__(self):
        self.entries = []

    @staticmethod
    def intersects(mbr1, mbr2):
        return not (mbr1[2] < mbr2[0] or mbr1[0] > mbr2[2] or mbr1[3] < mbr2[1] or mbr1[1] > mbr2[3])

    def insert(self, mbr, item_id):
        self.entries.append((mbr, item_id))

    def query(self, search_mbr):
        results = []
        for mbr, item_id in self.entries:
            if SimpleRTree.intersects(mbr, search_mbr):
                results.append(item_id)
        return results
