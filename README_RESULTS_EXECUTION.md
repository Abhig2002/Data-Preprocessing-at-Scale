# Results Execution Guide – Graph & Streaming Portfolio

This document records the execution steps and observed results for the combined
graph processing and distributed streaming projects.

The purpose of this file is to:
- Execute the full pipeline end-to-end
- Capture visual evidence for the portfolio Results section
- Avoid copying code, logs, or configuration into the report

---

## Project 1: Graph Data Processing Results

### Step 1: Start Neo4j Environment
Ensure the Neo4j container is running and accessible through the Neo4j Browser
(web interface).

Expected outcome:
- Neo4j Browser loads successfully
- Database is running without errors

(No screenshots needed here)

---

### Step 2: Verify Graph Structure

Run the following query only to generate the visualization.
Do NOT include the query text in screenshots.

MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 50

Expected observation:
- Nodes labeled as Location
- Directed relationships labeled TRIP
- Graph shows connected structure

Capture Screenshot:
- Graph visualization pane only
- Crop out query editor and results table

---

### Step 3 (Optional): BFS Path Visualization

Run this query to visualize a shortest path between two locations
(use any two valid location IDs).

MATCH (start:Location {location_id: 1}), (end:Location {location_id: 50})
MATCH p = shortestPath((start)-[:TRIP*..10]->(end))
RETURN p

Expected observation:
- A highlighted path connecting two nodes
- Demonstrates reachability in the graph

Optional Screenshot:
- Visualization only
- Crop out query text

---

### Algorithm Execution (No Visualization Required)

The following algorithms were executed successfully:
- PageRank
- Breadth-First Search

Results will be described in text only in the portfolio report.
No screenshots or numeric outputs are required.

---

## Project 2: Distributed Streaming Pipeline Results

### Step 4: Verify Kubernetes Deployment

Run the following commands in the terminal:

kubectl get pods
kubectl get services

Expected observation:
- All pods in Running state
- Services exposed for Kafka and Neo4j

Capture Screenshot:
- Terminal output only
- Show both commands
- Crop tightly (no command history, no scrolling)

---

### Step 5: Execute Data Producer

Run the producer script to stream trip records into Kafka.

Expected observation:
- Records are published continuously
- No runtime errors

(No screenshots needed here)

---

### Step 6: Verify Streaming Ingestion in Neo4j

After the producer has been running, open Neo4j Browser and run:

MATCH (n)-[r]->(m)
RETURN n, r, m
LIMIT 50

Expected observation:
- New nodes and relationships appear
- Graph updates as streaming progresses
- Structure matches Project 1 schema

Capture Screenshot:
- Graph visualization only
- Crop out query editor

---

## Summary of Captured Artifacts

Project 1:
- Graph structure visualization
- (Optional) BFS path visualization

Project 2:
- Kubernetes pods + services terminal screenshot
- Neo4j streamed graph visualization

These artifacts will be referenced as figures in the portfolio Results section.
No code or logs will be included in the final report.
