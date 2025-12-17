# Project 2: Data Processing Pipeline

**Course:** CSE 511: Data Processing at Scale  
**Instructor:** Zhichao Cao, Ph.D.

---

## 🧠 Introduction

This project extends the previous Docker + Neo4j setup into a scalable, high-availability data processing pipeline using **Kubernetes (Minikube)** and **Kafka**.  
The system ingests streaming documents, processes them in real time, and stores graph-structured data in **Neo4j** for analytics such as **PageRank** and **Breadth-First Search (BFS)**.

---

## ⚙️ System Architecture

### Component Roles

| Component | Role / Function |
|------------|------------------|
| **Minikube** | A local Kubernetes cluster that orchestrates and manages all containerized components (Kafka, Zookeeper, Neo4j, etc.) on your machine. It simulates a real Kubernetes environment for development and testing. |
| **kubectl** | The command-line tool for interacting with Kubernetes. It’s used to deploy YAML files, monitor pods and services, and manage cluster resources (e.g., `kubectl apply -f kafka.yaml`, `kubectl get pods`). |
| **Helm** | A package manager for Kubernetes (like `apt` or `pip`). It simplifies installing and managing complex applications — for example, deploying Neo4j using a single Helm chart instead of multiple YAML files. |
| **Zookeeper** | A coordination service that manages and tracks Kafka brokers, ensuring reliability, synchronization, and configuration consistency. |
| **Kafka** | A distributed message streaming platform that ingests data from producers and distributes it to consumers (e.g., Kafka Connect). It enables high-throughput, real-time data flow between components. |
| **Kafka Connect** | A data integration layer for Kafka that connects topics to external systems like databases. In this project, it pushes streaming data from Kafka into Neo4j using the Neo4j connector. |
| **Neo4j** | A graph database used for storing, querying, and analyzing connected data. It runs graph algorithms such as PageRank and BFS on the streamed data. |

📂 **Additional Resources:**  
[Dropbox Project Files](https://www.dropbox.com/scl/fo/jzi0zjchxwp3ekcnzv63f/APpxPyUIwuR0S-f6aHMpVvs?rlkey=p1qo00qyvzh1dfehl6bsyo8ow&st=p082gm3t&dl=0)

---

## 🪛 Step 0: Environment Setup (0 pts)

Set up the orchestrator and Kafka for your pipeline.

- The orchestrator helps manage ingestion, processing, and storage components.
- You will use **Minikube** as the orchestrator — a lightweight Kubernetes implementation that runs locally.

---

## 🐝 Step 1: Kafka & ZooKeeper Setup

You will use Kafka to ingest data from the document stream and distribute it to other components of your pipeline.

A **YAML file** tells Kubernetes what to create and how it should behave (containers, services, etc.). You define two objects for each component:

1. **Deployment** → runs your containers (the “brains”).
2. **Service** → exposes them inside or outside the cluster (the “network interface”).

### 🧩 What to Implement

Two YAML files are provided:

- `zookeeper-setup.yaml` → Complete it with **service** information.
- `kafka-setup.yaml` → Complete it with **deployment** information.

### ⚙️ Required Configurations (for `kafka-setup.yaml`)

```yaml
image: confluentinc/cp-kafka:7.3.3
KAFKA_BROKER_ID: "1"
KAFKA_ZOOKEEPER_CONNECT: "zookeeper-service:2181"
KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: "PLAINTEXT:PLAINTEXT,PLAINTEXT_INTERNAL:PLAINTEXT"
KAFKA_ADVERTISED_LISTENERS: "PLAINTEXT://localhost:9092,PLAINTEXT_INTERNAL://kafka-service:29092"
KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: "1"
KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"
```

> 📝 **Note:** Minikube may start with limited resources. Increase them if necessary when starting Minikube.

---

## 🧩 Step 2: Neo4j Deployment

You’ll deploy **Neo4j** in Kubernetes. Since data will be streamed, use existing Neo4j Kubernetes setups.

A file `neo4j-service.yaml` is provided — modify it to start a Neo4j service accessible at `neo4j-service:7474` within the Minikube network.

📖 **Reference:** [Neo4j Kubernetes Documentation](https://neo4j.com/docs/operations-manual/current/kubernetes/)

### 🧱 What to Implement

Create a file `neo4j-values.yaml` with the following:

- Set the **password** to `processingpipeline`.
- Ensure the **GDS (Graph Data Science)** library is installed.

---

## 🔄 Step 3: Neo4j ↔ Kafka Connection

Now connect Kafka and Neo4j using **Kafka Connect**.

### 🧱 What to Implement

Create `kafka-neo4j-connector.yaml` — a YAML file that launches a custom image converting Kafka topic data into Neo4j-compatible data.

📚 **References:**
- [Kafka Connect Neo4j Docs](https://neo4j.com/docs/kafka/)
- [DockerHub Custom Image](https://hub.docker.com/r/change1472/cse511-kafka-neo4j-connector)

### 🧩 Image to Use

```yaml
image: change1472/cse511-kafka-neo4j-connector
```

> **Use:**
> - `latest` tag for **amd64** (Intel/AMD) systems.
> - `arm64` tag for **Apple Silicon (M1/M2)** Macs.

📦 A Dockerfile for this step is available in the Dropbox folder for reference.

---

## 🧪 Step 4: Pipeline Testing & Analytics

After completing the setup:

- Run the provided `data_producer.py` file.
- Data flow should follow:

```
producer → kubernetes → kafka → neo4j → analytics
```

- After data loads into Neo4j, run `tester.py` to verify functionality.
- Ensure ports are exposed outside the Minikube environment. Use `grader.md` as a reference.

> 💡 If you face connection issues during `data_producer`, ensure `KAFKA_ADVERTISED_LISTENERS` is correctly set to:
> ```
> PLAINTEXT://localhost:9092,PLAINTEXT_INTERNAL://kafka-service:29092
> ```

---

## 📦 Submission Requirements & Guidelines

### 📁 What to Submit on Canvas

Create a ZIP file containing:

1. `zookeeper-setup.yaml`
2. `kafka-setup.yaml`
3. `neo4j-values.yaml`
4. `kafka-neo4j-connector.yaml`

### 🧾 File Naming Convention

- Name your ZIP file as your **ASU 10-digit ID** (e.g., `1221234567.zip`).
- Incorrect filenames or additional files incur a **30-point penalty.**

---

## 🕒 Submission Policies

1. **No late submissions.** Only on-time submissions are graded unless a verifiable emergency is proven.
2. **Submit partial work** if incomplete to earn partial credit.
3. **Individual work only.**
   - High-level conceptual discussion is allowed.
   - Code-level discussion or sharing is prohibited.
   - Violations result in course failure. Plagiarism tools will be used.

---

## 🧮 Grading Rubric (100 pts)

| Section | Description | Points |
|----------|--------------|---------|
| Step 0 | Environment Setup | 0 |
| Step 1 | Kafka & Zookeeper YAML configuration | 25 |
| Step 2 | Neo4j Deployment and Configuration | 25 |
| Step 3 | Kafka ↔ Neo4j Connection (Connector YAML) | 25 |
| Step 4 | Pipeline Testing & Analytics | 25 |

---

**End of Document**  
*© 2025 Zhichao Cao, Ph.D.*

