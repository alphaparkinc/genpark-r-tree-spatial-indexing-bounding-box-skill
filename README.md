# R-Tree Spatial Indexing Skill

Hierarchical bounding volume spatial indexing engine for fast 2D range searching and geometric collision detection.

```mermaid
flowchart TD
    Box["Insert 2D MBR [min_x, min_y, max_x, max_y]"] --> Tree["Spatial Index Entries"]
    Query["Search Box Query Window"] --> Filter["MBR Intersection Test: Non-disjoint Intervals"]
    Filter --> Results["Candidate Spatial Intersection IDs"]
```

## Features
- **100% Python Standard Library**: No external spatial C-libraries.
- **Fast Bounding Box Filtering**: Sublinear spatial query efficiency.
