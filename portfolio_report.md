## Graph-Based and Streaming Data Processing with Neo4j, Kafka, and Kubernetes  
### CSE 511 Project Portfolio

**Author**: Abhisekhar Bharadwaj Gandavarapu  
**Course**: CSE 511 – Data Processing at Scale  

---

## Introduction  

This project portfolio documents my work for CSE 511: Data Processing at Scale, combining two closely related projects into a single, unified system. The first project focused on graph data processing using Neo4j and Docker, while the second extended this foundation into a distributed streaming pipeline using Kafka, Kubernetes, and Neo4j. Both projects were built around real-world taxi trip data from New York City, with an emphasis on modeling trips as a graph and then processing that graph at scale.  

The overall motivation was to understand how modern data platforms can support both batch-style graph analytics and near-real-time streaming workloads. In the first phase, I learned how to transform a raw tabular dataset into a graph structure and apply standard graph algorithms such as PageRank and breadth-first search (BFS). In the second phase, I learned how to treat the same dataset as a stream of events, route it through Kafka topics, and continuously load it into a Neo4j graph running inside a Kubernetes cluster. Together, these projects form a small but complete pipeline from raw files to a running graph database that can support both static and streaming analysis.  

By the end of the portfolio, I had a working Dockerized Neo4j instance loaded with New York City yellow taxi data, graph algorithms implemented over that data, and a distributed pipeline that ingested filtered taxi trips into Neo4j via Kafka and Kubernetes. This report explains the architecture, data flow, and results at a conceptual level and reflects on the skills I gained in the process.  

---

## Explanation of the Solution  

### Graph Data Processing (Project 1)  

In the first project, I built a graph-based view of New York City taxi trips, using Neo4j as the graph database engine. The starting point was the March 2022 yellow taxi trip dataset, which records individual trips with pickup and drop-off times, pickup and drop-off location identifiers, trip distance, and fare information. Instead of treating this as a purely relational or tabular dataset, I modeled it as a graph where geographic zones are nodes and trips are edges between those zones.  

Conceptually, each distinct taxi zone was represented as a location node, identified by a numeric location identifier. Each individual trip became a directed relationship connecting a pickup location node to a drop-off location node. The relationship carried key properties such as distance, fare, and pickup and drop-off timestamps. This graph structure captures both the topology of movements across the city and relevant attributes needed for analysis, such as how far people travel and how much they pay.  

To make the project manageable and interesting, I focused on a subset of the city: trips that start and end in Bronx-related zones, and that exceed minimum thresholds for distance and fare. Conceptually, this filtering step removed very short or low-value trips and limited the graph to a coherent geographic region. I implemented a data loading workflow that reads the parquet file, filters and cleans the data (for example, selecting required columns, applying thresholds, and converting timestamps into a Neo4j-friendly datetime format), and then bulk-loads the results into Neo4j by creating or merging location nodes and creating trip relationships.  

The Neo4j instance itself was encapsulated in a Docker image. The Docker environment was responsible for installing and configuring Neo4j, installing the necessary Python and graph libraries, enabling the Graph Data Science (GDS) plugin, and preparing the database to accept connections. When the container starts, it exposes the Neo4j HTTP and Bolt ports to the host, allowing an external client script to connect and run graph algorithms once the data has been loaded.  

On top of this graph, I implemented two classical graph algorithms using Neo4j and the GDS library: PageRank and breadth-first search. The PageRank component treats each location node as a vertex whose importance is determined by the structure of incoming and outgoing trip relationships. I projected the graph into the GDS in-memory representation, ran PageRank with a configurable maximum number of iterations and a configurable edge-weight property (such as distance or fare), and then examined which locations achieved the highest and lowest scores. This revealed which zones are central or peripheral within the filtered Bronx taxi network.  

The BFS component focused on reachability and path discovery across the same graph. Conceptually, it takes a starting location and a target location and searches for a path through the trip relationships. In practice, I used the graph structure defined in Neo4j to identify a sequence of locations that connect the start to the target, respecting the direction of travel along the trips. The result is a simple path expressed as an ordered list of locations that shows how a traveler might move from one part of the Bronx to another through observed taxi traffic.  

### Distributed Streaming Pipeline (Project 2)  

The second project built on the same New York City taxi data but treated the dataset as a stream of events flowing through a distributed system. Instead of loading all trips into Neo4j in one batch, I implemented a Kafka-based pipeline where taxi trips are produced as messages to a Kafka topic, processed through a connector, and ultimately written into a Neo4j graph running in a Kubernetes cluster.  

At the source of the pipeline is a data producer process. Conceptually, this component reads the same parquet file as before, selects a subset of relevant columns, filters for Bronx-related trips, and applies the same basic thresholds on distance and fare. Instead of directly writing to a database, it iterates over the resulting rows and converts each one into a compact message format, such as a JSON representation of distance, pickup and drop-off zones, and fare. Each message is then sent to a Kafka topic dedicated to New York City taxi data. This transforms the static dataset into a stream of trip events that can be consumed in real time.  

Kafka itself, along with Zookeeper, is deployed on Kubernetes using declarative manifests. In the grading environment, a local Kubernetes cluster (for example, via Minikube) is used, and the Zookeeper and Kafka deployments are applied to the cluster using standard Kubernetes commands. Once the Kafka pods and services are running, they expose a bootstrap address that the producer can use to publish messages.  

Neo4j is also deployed inside the same Kubernetes cluster using a Helm chart. A custom values file configures the Neo4j instance and an additional service manifest exposes Neo4j’s ports so that external tools and the pipeline components can communicate with it. This makes Neo4j an internal service within the cluster while still allowing connections from outside when needed for testing or exploration.  

Between Kafka and Neo4j sits a connector component, deployed as another pod in the cluster. Conceptually, this connector subscribes to the taxi data topic, consumes the incoming messages, and translates them into write operations against Neo4j. The connector container image is prebuilt and is configured through environment variables so that it knows how to connect to Kafka (via the Kafka service) and where to send data in Neo4j. The end result is an automated path from each produced Kafka message to the creation or update of nodes and relationships inside the Neo4j graph.  

To validate the entire pipeline, I relied on port-forwarding from Kubernetes services to the local machine. By forwarding the Kafka and Neo4j services, I could run the data producer on my host, have it publish messages to Kafka in the cluster, and then inspect the resulting graph in Neo4j via the standard user interface or client scripts. In this way, the two projects become one integrated system: the same conceptual graph model is first constructed via batch loading and then fed incrementally via a streaming pipeline.  

---

## Description of the Results  

From the graph processing perspective, I was able to build the Docker image for Neo4j, start a container, and successfully load the filtered Bronx subset of the March 2022 yellow taxi dataset. After the loading step completed, a quick visual inspection of the graph confirmed that location nodes existed for the expected range of Bronx location identifiers and that each trip relationship stored distance, fare, and timestamp information. Simple exploratory queries, such as listing a sample of nodes and relationships, showed that the schema and properties matched the intended design.  

Running PageRank on this graph produced a ranking of locations by their structural importance within the Bronx taxi movement network. Locations that appeared as frequent hubs—either because many trips originated there or because they connected multiple parts of the borough—received higher scores, while less frequently used zones or those on the periphery of the graph received lower scores. The algorithm converged within the specified number of iterations and returned a consistent ordering of locations, which suggests that the graph projection and configuration were correct.  

For BFS, I tested paths between chosen pairs of Bronx locations. When a path existed, the BFS-based query returned a sequence of intermediate locations, effectively showing how a traveler could move step by step from the start zone to the target zone via observed taxi trips. In cases where there was no path under the given constraints, the query correctly reported an empty result. These tests gave me confidence that the underlying graph connectivity and relationships were correctly captured.  

In the streaming pipeline, I verified that the Kafka producer could connect to the Kafka cluster running in Kubernetes by inspecting the available topics and confirming that the New York City taxi topic was recognized. As the producer iterated over the filtered dataset, it printed a running counter and confirmation messages, indicating that records were being successfully sent to the topic. On the Kubernetes side, the Kafka pods remained healthy, and the connector deployment came up with the correct environment configuration.  

After running the producer for some time, I inspected the Neo4j instance deployed in Kubernetes. The presence of newly created nodes and relationships that matched the semantics of the taxi trips indicated that the connector was consuming messages and translating them into graph updates. This demonstrated an end-to-end flow: a file-based dataset was transformed into a stream of Kafka messages, and those messages were then materialized as graph structures in Neo4j inside the cluster. Subsequent tests using the existing graph algorithms confirmed that the graph produced through streaming ingestion remained compatible with the analytics implemented in the first project.  

---

## Contributions  

This portfolio represents an individual project completed solely by me. I was responsible for the design, implementation, configuration, and debugging across both Project 1 and Project 2.  

My main contributions in Project 1 included designing the graph schema for the New York City taxi data, deciding to focus on Bronx-related zones, and implementing the data cleaning and transformation logic that converts raw parquet records into a graph-friendly format. I implemented the workflow that loads the filtered records into Neo4j as location nodes and trip relationships, ensuring that the properties were correctly typed and indexed where appropriate. I also configured and validated the Docker environment for Neo4j, including enabling the Graph Data Science plugin needed to run PageRank.  

On top of the data model, I implemented the two core graph algorithms required for this project. I set up the in-memory GDS graph projection and PageRank configuration to compute centrality scores across locations, and I implemented the BFS-based logic to find paths between pairs of locations. I tested both components against the loaded graph to ensure that the results were reasonable and consistent with the underlying data.  

In Project 2, I implemented the Kafka data producer that streams filtered taxi trips into Kafka. I reused the Bronx-focused filtering logic conceptually, restructured the relevant attributes into compact messages, and ensured that the producer could sustain a steady flow of records while respecting the expected Kafka configuration. I also prepared and used Kubernetes manifests for Zookeeper, Kafka, Neo4j, and the Kafka–Neo4j connector, and I handled the integration details such as service naming, environment variables, and port-forwarding required to make the system work as a whole.  

Across both projects, I was responsible for orchestrating and testing the entire pipeline—from building and running Docker containers through to deploying and interacting with services in Kubernetes, verifying that the graph remained analyzable with the same algorithms regardless of whether the data arrived via batch loading or via streaming.  

---

## Skills, Techniques, and Knowledge Gained  

Working on this combined portfolio gave me practical experience with several modern data processing technologies and concepts. First, I gained a much deeper understanding of graph data modeling in Neo4j. Instead of thinking only in tables and joins, I learned to describe real-world systems—like urban mobility—using nodes and relationships, and to reason about connectivity and centrality in that context. I also practiced writing and interpreting graph queries and using higher-level graph analytics through the Graph Data Science library.  

Second, I learned how to package a graph database into a reproducible Docker image and how to configure it programmatically. This included handling installation of dependencies, enabling plugins, setting configuration parameters, and ensuring that the container could be built and run non-interactively. This experience made me more comfortable with treating infrastructure as code and understanding how environment setup affects application behavior.  

Third, I developed a working understanding of Kafka as a distributed messaging system. I learned how to configure a producer, create topics, and monitor message flow. More importantly, I experienced how a static dataset can be reinterpreted as a stream of events and how that changes the way we design downstream consumers and storage systems.  

Fourth, I gained exposure to Kubernetes as a platform for orchestrating distributed systems. I worked with deployments, services, and Helm charts to bring up coordinated sets of pods, including Zookeeper, Kafka, Neo4j, and the connector. Through port-forwarding and basic troubleshooting, I developed an intuition for how services communicate inside a cluster and how to make them accessible from outside for testing.  

Finally, at a higher level, I learned how to reason about end-to-end data pipelines that combine multiple technologies. Connecting batch processing, graph analytics, message streaming, and container orchestration gave me a more integrated view of data processing at scale and helped me appreciate the trade-offs between one-time bulk loading and continuous ingestion.  

---

## References  

[1] Neo4j, “Neo4j Graph Database Platform Documentation,” Neo4j, accessed Dec. 2025. Online: `https://neo4j.com/docs/`  

[2] Neo4j, “Graph Data Science Library Documentation,” Neo4j, accessed Dec. 2025. Online: `https://neo4j.com/docs/graph-data-science/`  

[3] Apache Software Foundation, “Apache Kafka Documentation,” Apache Kafka, accessed Dec. 2025. Online: `https://kafka.apache.org/documentation/`  

[4] Cloud Native Computing Foundation, “Kubernetes Documentation,” Kubernetes, accessed Dec. 2025. Online: `https://kubernetes.io/docs/`  

[5] New York City Taxi and Limousine Commission, “Yellow Taxi Trip Records: Data Dictionary,” NYC TLC, accessed Dec. 2025. Online: `https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page`  


