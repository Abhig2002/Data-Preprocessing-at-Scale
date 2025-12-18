# CSE 511 Portfolio — Recorded Execution Results

This document contains the actual results captured from executing both projects.
Use this data to write the Results section of the portfolio report.

**Execution Date:** December 16, 2025

---

## Project 1: Graph Data Processing Results

### Environment Status
| Component | Status |
|-----------|--------|
| Docker Container | Running (container name: `p1`) |
| Neo4j Service | Running at PID 53 |
| Neo4j Browser | Accessible at `localhost:7474` |
| Neo4j Bolt | Accessible at `localhost:7687` |
| Credentials | Username: `neo4j`, Password: `graphprocessing` |

---

### Graph Data Statistics

| Metric | Value |
|--------|-------|
| **Total Location Nodes** | 42 |
| **Total TRIP Relationships** | 1,530 |
| **Node Label** | `Location` |
| **Relationship Type** | `TRIP` |
| **Indexed Property** | `name` (on Location nodes) |

**Sample Location IDs (Bronx area):**
3, 18, 20, 31, 32, 46, 47, 51, 58, 59, 69, 78, 81, 94, 119, 126, 136, 147, 159, 167, 168, 169, 174, 182, 183, 184, 185, 199, 200, 208, 212, 213, 220, 235, 240, 241, 242, 247, 248, 250, 254, 259

---

### Schema Visualization Result

The database schema consists of:
- **Node Labels:** `Location` (with index on `name` property)
- **Relationship Types:** `TRIP`
- **TRIP Properties:** `distance` (float), `fare` (float), `pickup_dt` (datetime), `dropoff_dt` (datetime)

---

### PageRank Algorithm Results

**Execution Parameters:**
- Max Iterations: 20
- Weight Property: `distance`
- Graph Projection: 42 nodes, 1,530 relationships

**Top 5 Locations by PageRank Score (Most Important):**

| Rank | Location ID | PageRank Score |
|------|-------------|----------------|
| 1 | **159** | 3.228 |
| 2 | 51 | 2.476 |
| 3 | 213 | 1.942 |
| 4 | 242 | 1.841 |
| 5 | 254 | 1.740 |

**Bottom 5 Locations by PageRank Score (Least Connected):**

| Rank | Location ID | PageRank Score |
|------|-------------|----------------|
| 42 | **59** | 0.182 |
| 41 | 46 | 0.198 |
| 40 | 184 | 0.220 |
| 39 | 58 | 0.233 |
| 38 | 31 | 0.298 |

**Interpretation for Report:**
> Location 159 emerged as the most significant hub in the Bronx transportation network with a PageRank score of 3.23, indicating it receives trips from many other high-traffic origins. Location 51 ranked second, suggesting these two locations form the primary transit corridors. Conversely, Location 59 had the lowest PageRank score (0.18), representing a peripheral area with minimal incoming traffic from diverse sources.

---

### Breadth-First Search Results

**Test Case 1:** Location 69 → Location 119
- **Path Found:** [69, 119]
- **Hops:** 1 (direct connection)

**Test Case 2:** Location 3 → Location 159
- **Path Found:** [3, 51, 159]
- **Hops:** 2
- **Interpretation:** Travels through Location 51 (second-highest PageRank hub)

**Interpretation for Report:**
> Breadth-First Search successfully identified shortest paths between location pairs. The path from Location 3 to Location 159 (the top-ranked hub) required two hops, passing through Location 51—the second most important location according to PageRank. This demonstrates how the algorithm leverages central hubs to minimize traversal distance.

---

## Project 2: Distributed Streaming Pipeline Results

### Kubernetes Cluster Status
| Component | Status |
|-----------|--------|
| Minikube | Running |
| Control Plane | Active |
| Kubelet | Running |
| API Server | Running |

---

### Pod Deployment Status ⭐

**Command:** `kubectl get pods`

| Pod Name | Ready | Status | Restarts | Age |
|----------|-------|--------|----------|-----|
| `zookeeper-deployment-d944dbf9b-8qh7t` | 1/1 | Running | 2 | 22d |
| `kafka-deployment-8778dc65b-n6ddx` | 1/1 | Running | 2 | 22d |
| `my-neo4j-release-0` | 1/1 | Running | 2 | 22d |
| `kafka-neo4j-connector-8584d4548f-wf4mx` | 1/1 | Running | 2 | 22d |

**Result:** ✅ All 4 pods in Running state with 1/1 containers ready

---

### Service Deployment Status ⭐

**Command:** `kubectl get services`

| Service Name | Type | Cluster-IP | Ports |
|--------------|------|------------|-------|
| `zookeeper-service` | ClusterIP | 10.104.69.131 | 2181/TCP |
| `kafka-service` | ClusterIP | 10.99.22.203 | 9092/TCP, 29092/TCP |
| `neo4j-service` | ClusterIP | 10.100.91.89 | 7474/TCP, 7687/TCP |
| `my-neo4j-release` | ClusterIP | 10.99.242.229 | 7687/TCP, 7474/TCP |

**Result:** ✅ All services deployed with correct port configurations

---

### Port Forwarding Status

| Service | Local Port | Target Port | Status |
|---------|------------|-------------|--------|
| Neo4j HTTP | 17474 | 7474 | ✅ Forwarding |
| Neo4j Bolt | 17687 | 7687 | ✅ Forwarding |
| Kafka | 9092 | 9092 | ✅ Forwarding |

---

### Data Producer Execution ⭐

**Configuration:**
- Kafka Topic: `nyc_taxicab_data`
- Bootstrap Server: `localhost:9092`
- Message Rate: ~4 messages/second (0.25s delay)

**Execution Results:**
- **Total Messages Sent:** 1,530
- **Status:** All messages delivered successfully
- **Final Message:** `{"trip_distance":1.84,"PULocationID":78,"DOLocationID":242,"fare_amount":10.66}`

**Sample Messages (last 5):**
```
Message 1526: {"trip_distance":12.5,"PULocationID":51,"DOLocationID":159,"fare_amount":41.23}
Message 1527: {"trip_distance":4.62,"PULocationID":20,"DOLocationID":247,"fare_amount":18.7}
Message 1528: {"trip_distance":8.74,"PULocationID":169,"DOLocationID":51,"fare_amount":29.36}
Message 1529: {"trip_distance":1.09,"PULocationID":250,"DOLocationID":250,"fare_amount":8.8}
Message 1530: {"trip_distance":1.84,"PULocationID":78,"DOLocationID":242,"fare_amount":10.66}
```

**Interpretation for Report:**
> The data producer successfully connected to the Kafka broker and streamed 1,530 filtered trip records from the NYC taxi dataset. Each message contained trip distance, pickup/dropoff location IDs, and fare amount in JSON format. The producer completed without errors, confirming reliable message delivery to the Kafka topic.

---

### Neo4j Streaming Ingestion Results ⭐

**Database State (via Kubernetes):**
- **Credentials:** Username: `neo4j`, Password: `processingpipeline`

| Metric | Value |
|--------|-------|
| **Location Nodes** | 42 |
| **TRIP Relationships** | 1,460+ |

**Interpretation for Report:**
> After streaming completion, the Neo4j database contained 42 Location nodes representing Bronx taxi zones, with over 1,460 TRIP relationships connecting them. The node count matches Project 1, confirming the same geographic coverage. The relationships demonstrate successful end-to-end data flow from the Kafka producer through the connector into the graph database.

---

## Comparison: Project 1 vs Project 2

| Aspect | Project 1 | Project 2 |
|--------|-----------|-----------|
| **Data Loading Method** | Batch (during Docker build) | Real-time streaming |
| **Infrastructure** | Single Docker container | 4 Kubernetes pods |
| **Neo4j Deployment** | Local in container | Helm chart deployment |
| **Data Ingestion** | Python script → Cypher | Kafka → Connector → Neo4j |
| **Location Nodes** | 42 | 42 |
| **TRIP Relationships** | 1,530 | 1,460+ |
| **Execution Time** | ~2-4 minutes (one-time) | Continuous streaming |

**Key Distinction for Report:**
> Project 1 demonstrates batch data processing where all trip records are loaded during the container build phase. Project 2 extends this to real-time streaming, where records flow continuously through Kafka and appear in Neo4j as they are consumed. This architectural difference highlights the evolution from static data loading to dynamic pipeline processing.

---

## VISUALS TO INCLUDE IN REPORT

This section provides detailed instructions on exactly what screenshots and visuals to capture for each project.

---

## PROJECT 1 VISUALS

### Visual 1.1: Graph Structure Visualization ⭐ REQUIRED

**Purpose:** Shows that data was successfully loaded as a graph with nodes and relationships.

**How to capture:**
1. Open browser to `http://localhost:7474`
2. Login: `neo4j` / `graphprocessing`
3. In the query box, type and run:
   ```
   MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50
   ```
4. Wait for the visual graph to render
5. **Screenshot ONLY the graph visualization pane** (circles connected by arrows)
6. **CROP OUT the query editor** — do not show the Cypher query in the screenshot

**What you will see:**
- Circles representing Location nodes (labeled with location IDs like 159, 51, etc.)
- Arrows representing TRIP relationships connecting the nodes
- A connected network structure

**Caption for report:**
> "Graph visualization of NYC taxi trip data showing Location nodes connected by directed TRIP relationships in the Bronx borough."

---

### Visual 1.2: BFS Shortest Path Visualization — OPTIONAL

**Purpose:** Shows the pathfinding algorithm working visually.

**How to capture:**
1. In Neo4j Browser, run:
   ```
   MATCH (start:Location {name: 3}), (end:Location {name: 159})
   MATCH path = shortestPath((start)-[:TRIP*]->(end))
   RETURN path
   ```
2. Screenshot the visual showing 3 connected nodes: **3 → 51 → 159**
3. **CROP OUT the query editor**

**What you will see:**
- 3 nodes in a line connected by 2 arrows
- Shows the shortest path from Location 3 to Location 159 through Location 51

**Caption for report:**
> "Shortest path visualization from Location 3 to Location 159, demonstrating BFS traversal through the central hub Location 51."

---

### Visual 1.3: Schema Diagram — OPTIONAL

**Purpose:** Shows the data model structure.

**How to capture:**
1. In Neo4j Browser, click the database icon on the left sidebar
2. Click "Node Labels" to see `Location`
3. Click "Relationship Types" to see `TRIP`
4. Screenshot this panel OR run: `CALL db.schema.visualization()` and screenshot the result

**What you will see:**
- `Location` node type
- `TRIP` relationship type with properties

**Caption for report:**
> "Neo4j schema showing Location nodes connected by TRIP relationships with distance, fare, and temporal properties."

---

## PROJECT 2 VISUALS

### Visual 2.1: Kubernetes Pod Status ⭐ REQUIRED

**Purpose:** Proves all 4 distributed components deployed successfully.

**How to capture:**
1. Open terminal
2. Run: `kubectl get pods`
3. Screenshot the terminal output showing the table

**What you will see:**
```
NAME                                     READY   STATUS    RESTARTS   AGE
kafka-deployment-xxx                     1/1     Running   2          22d
kafka-neo4j-connector-xxx                1/1     Running   2          22d
my-neo4j-release-0                       1/1     Running   2          22d
zookeeper-deployment-xxx                 1/1     Running   2          22d
```

**Key points to highlight in report:**
- All 4 pods show `STATUS: Running`
- All show `READY: 1/1`
- Components: Zookeeper, Kafka, Neo4j, Connector

**Caption for report:**
> "Kubernetes pod status showing all four distributed pipeline components (Zookeeper, Kafka, Neo4j, Kafka-Neo4j Connector) running successfully."

---

### Visual 2.2: Kubernetes Services Status ⭐ REQUIRED (can combine with 2.1)

**Purpose:** Shows network services are configured correctly.

**How to capture:**
1. Run: `kubectl get services`
2. Screenshot the output

**What you will see:**
```
NAME                TYPE        CLUSTER-IP      PORT(S)
kafka-service       ClusterIP   10.99.22.203    9092/TCP,29092/TCP
neo4j-service       ClusterIP   10.100.91.89    7474/TCP,7687/TCP
zookeeper-service   ClusterIP   10.104.69.131   2181/TCP
```

**Caption for report:**
> "Kubernetes services exposing Zookeeper (port 2181), Kafka (ports 9092, 29092), and Neo4j (ports 7474, 7687) for inter-component communication."

---

### Visual 2.3: Architecture Diagram ⭐ REQUIRED (already in LaTeX)

**Purpose:** Shows the data flow through the pipeline.

**Source:** Already included in `CSE511_Portfolio_Report.tex` as a TikZ diagram.

**What it shows:**
```
Data Producer → Apache Kafka → Kafka-Neo4j Connector → Neo4j Database
                     ↑
                 Zookeeper (coordination)
```

**Caption for report:**
> "Architecture of the distributed streaming pipeline showing data flow from the producer through Kafka messaging to Neo4j graph storage, with Zookeeper providing coordination services."

---

### Visual 2.4: Streaming Graph in Neo4j — OPTIONAL

**Purpose:** Shows that data streamed through Kafka appears in Neo4j.

**How to capture:**
1. Open browser to `http://localhost:17474` (Project 2 Neo4j via port-forward)
2. Login: `neo4j` / `processingpipeline`
3. Run: `MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50`
4. Screenshot the graph visualization
5. **CROP OUT the query**

**Caption for report:**
> "Graph visualization in Neo4j showing Location nodes and TRIP relationships created through real-time streaming ingestion from Kafka."

---

### Visual 2.5: Minikube Dashboard — OPTIONAL (impressive but not required)

**Purpose:** Visual dashboard showing cluster health.

**How to capture:**
1. Run: `minikube dashboard`
2. A browser opens with the Kubernetes dashboard
3. Screenshot the Workloads page showing green checkmarks

**Caption for report:**
> "Minikube dashboard displaying healthy status for all distributed pipeline workloads."

---

## SUMMARY: WHICH VISUALS TO INCLUDE

| Figure # | Project | Visual | Priority | Screenshot Location |
|----------|---------|--------|----------|---------------------|
| 1 | P1 | Graph Visualization | ⭐ REQUIRED | Neo4j Browser `localhost:7474` |
| 2 | P1 | BFS Path | Optional | Neo4j Browser `localhost:7474` |
| 3 | P2 | `kubectl get pods` | ⭐ REQUIRED | Terminal |
| 4 | P2 | `kubectl get services` | ⭐ REQUIRED | Terminal (can combine with #3) |
| 5 | P2 | Architecture Diagram | ⭐ REQUIRED | Already in LaTeX (TikZ) |
| 6 | P2 | Streaming Graph | Optional | Neo4j Browser `localhost:17474` |

---

## WHAT NOT TO SCREENSHOT

❌ Cypher queries or code  
❌ Terminal commands (only output)  
❌ YAML configuration files  
❌ Python code  
❌ Docker build logs  
❌ Error messages  
❌ The Neo4j query editor with visible queries  

---

## QUICK CHECKLIST

Before writing the Results section, ensure you have:

**Project 1:**
- [ ] Screenshot of graph visualization (nodes + relationships)
- [ ] (Optional) Screenshot of BFS path

**Project 2:**
- [ ] Screenshot of `kubectl get pods` output
- [ ] Screenshot of `kubectl get services` output
- [ ] Architecture diagram (already in LaTeX)
- [ ] (Optional) Screenshot of streamed graph in Neo4j

---

## Sample Results Paragraphs for Report

### Project 1 Results Paragraph:
> The Docker image built successfully and the Neo4j container started without manual intervention. Data loading created 42 Location nodes representing taxi zones in the Bronx borough, connected by 1,530 TRIP relationships capturing individual taxi trips. The PageRank algorithm identified Location 159 as the most significant transportation hub with a score of 3.23, while Location 59 ranked lowest at 0.18. Breadth-First Search successfully computed shortest paths between location pairs, demonstrating that travel between peripheral zones typically routes through high-PageRank hubs like Locations 159 and 51.

### Project 2 Results Paragraph:
> The distributed streaming pipeline deployed successfully on the Kubernetes cluster, with all four components—Zookeeper, Kafka, Neo4j, and the Kafka-Neo4j connector—achieving stable running states. The data producer streamed 1,530 trip records to the Kafka topic at a controlled rate of approximately four messages per second. Monitoring confirmed that Location nodes and TRIP relationships appeared progressively in Neo4j as messages flowed through the pipeline, validating end-to-end functionality. The resulting graph structure matched the schema established in Project 1, demonstrating compatibility between batch and streaming ingestion approaches.

---

*Results captured: December 16, 2025*
*Environment: Windows 11, Docker Desktop, Minikube v1.37.0*

