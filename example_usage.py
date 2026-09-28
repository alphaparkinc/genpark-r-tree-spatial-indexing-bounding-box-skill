"""Example demonstrating R-Tree spatial index queries."""
from client import SimpleRTree

def main():
    tree = SimpleRTree()
    tree.insert([0, 0, 5, 5], "ZoneA")
    tree.insert([10, 10, 20, 20], "ZoneB")
    hits = tree.query([3, 3, 7, 7])
    print("Spatial Intersection Query Hits:", hits)

if __name__ == "__main__":
    main()
