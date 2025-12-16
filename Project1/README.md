# Project 1: Graph Data Processing
**Course:** CSE 511: Data Processing at Scale

---

## Introduction

Graph data appears in the web, biology, transportation, and distributed systems. In this project, you will build a Dockerized Neo4j environment, load a real dataset, install the Graph Data Science (GDS) plugin, and implement two classic graph algorithms: PageRank and Breadth First Search (BFS).

---

## Step 0 — Exploring the world of Graph Databases (0 pts)

1. Create a free [Neo4j account](https://neo4j.com/cloud/platform/aura-graph-database/) to start exploring! They provide a variety of tools for developers, and in this part of the project, we are going to explore one of those tools: Neo4j Aura.
2. Create a new AuraDB instance (only the first instance is free). Go ahead and create that instance and load the provided Stack Overflow database.
3. Load the Stack Overflow sample and complete the guided tasks in the right-hand toolbar to learn Cypher and graph exploration.

---

## Step 1: Dockerfile & Data Loading (50 pts)

In this step, you will build a Docker container that installs Neo4j and loads the NYC taxi dataset into it. The schema of the NYC Trip dataset is available [here](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf). You can also go through this short [blog](https://medium.com/@NYCTLC/what-makes-a-city-street-smart-23496d92f60d) to understand how such datasets are making cities smarter.

You will learn how a Dockerfile is structured and how to set up your working environment. By the end of this step, you should be able to build and run your own Neo4j container, verify that the data has been loaded correctly, and confidently explore the database inside your container.

To get you started, we have already provided you with a template Dockerfile that performs various preliminary tasks like setting up the operating system and the target build platforms (so that your container can run on both ARM and x86). We have also provided you with a template `data_loader.py` file here. You need to write a query to load the data into the file. The schema you should follow is described below:

### Nodes
- Label: Location
- One node per pickup/dropoff locationID
- Property: name (locationID, integer), taken from PULocationID and DOLocationID

### Relationships
- Type: TRIP
- One relationship per trip
- Properties:
  - distance (float)
  - fare (float)
  - pickup_dt (datetime)
  - dropoff_dt (datetime)

> Important: Use exact labels and property names above. Datetimes may include a timezone or not; grading accepts either.

### Hints: High-Level Steps to Implement Step 1

Your Dockerfile must do the following:

1. Create a working directory: `/cse511/`
2. Download the [March 2022 NYC Taxi dataset](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet) inside the container.
3. Implement `data_loader.py` (before building the Docker image) and copy it from the same directory as your Dockerfile (relative path `./`) into `/cse511/` in the container.
   - The `data_loader.py` script will be executed in the RUN block later (see the end of the Dockerfile template).
   - Most of the setup logic has been provided in `data_loader.py`, so your main task is to load the data into Neo4j following the specified schema.
4. Install Java (OpenJDK 21):
   ```bash
   apt update
   apt install openjdk-21-jdk
   export JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
   ```
5. Upgrade pip and install only the required Python packages: `neo4j`, `pandas`, `pyarrow`
6. Install the Neo4j Graph Data Science (GDS) plugin v2.21.0:
   - Download from [Neo4j GDS releases](https://github.com/neo4j/graph-data-science/releases/)
   - Move it to `/var/lib/neo4j/plugins/`
7. Configure `/etc/neo4j/neo4j.conf` non-interactively by appending the required settings during the build process.
   - Allow Neo4j to listen on all network interfaces (0.0.0.0) so it can be accessed from the host.
   - Whitelist and enable unrestricted access to the APOC and GDS procedures.
   - Make these configuration updates automatically within the Docker build (for example, by appending lines to the neo4j.conf file).
   - Reference: [DigitalOcean configuration guide](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-neo4j-on-ubuntu-22-04#step-3-optional-configuring-neo4j-for-remote-access)
8. Set the default Neo4j password to `graphprocessing`.

If you have followed all the steps correctly, you will be able to create a Docker image using your Dockerfile, and on running a container using this instance, your Neo4j instance will be live. Then, your container is ready to perform operations. Port 7474 is exposed from inside Docker, which allows you to browse `localhost:7474` on your host machine and interact with your Neo4j browser directly.

Example queries:
```cypher
CALL db.schema.visualization();
MATCH (n) RETURN n LIMIT 25;
```

> Note: It takes 2-4 minutes for the server to be available after starting.

---

## Step 2: Implementing Graph Algorithms (50 pts)

With your Neo4j container up and the dataset loaded, implement the two algorithms below in `interface.py`. The `interface.py` file does not need to be inside the container and will connect to the Docker container from outside it (via port 7687).

> Note: Do not copy `interface.py` or `tester.py` into your Dockerfile build. During grading, the grader will only build your image using your `Dockerfile` and `data_loader.py` from the same folder—no other files are included. Bundling `interface.py` or `tester.py` in the image will cause grading errors.

### 1. PageRank (25 pts)

The PageRank algorithm evaluates the significance of each node in a graph by considering the number of incoming relationships and the importance of the source nodes that contribute to it. The basic premise is that a page's importance is determined by the pages that link to it.

The PageRank in the [original Google paper](http://infolab.stanford.edu/~backrub/google.html) is defined as below:

> We assume that page A has pages T1 to Tn, which point to it.  
> d is a damping factor between 0 (inclusive) and 1 (exclusive), usually set to 0.85.  
> C(A) is defined as the number of links going out of page A.  
> This equation is used to iteratively update a candidate solution and arrive at an approximate solution.

What to implement:
- Implement the PageRank algorithm using the GDS library.
- Consider `max_iter` and `weight_property`.
- Return nodes with maximum and minimum PageRank.

### 2. Breadth First Search (25 pts)

Breadth First Search (BFS) is a graph traversal algorithm that, given a start node, visits nodes in order of increasing distance. It supports various termination conditions such as reaching one of several target nodes, reaching the maximum depth, exhausting a given traversal budget, or traversing the entire graph.

What to implement:
- Implement BFS from location A to multiple locations.
- Use the variables `start_node` and `target_nodes`.
- You may use the Neo4j GDS library directly.

Reference: [Breadth-first search](https://en.wikipedia.org/wiki/Breadth-first_search)

---

## Grading

We expect to use your Docker file to create an image and deploy your container to test your code (`interface.py`). The Docker file MUST be able to perform the following steps without any manual intervention. Failure to do so will result in 0 grade points.

Do not edit any existing code in the template Docker file.

---

## Submission Requirements & Guidelines

### What to Submit on Canvas
Create a zip file containing the following:
- `Dockerfile`
- `interface.py`
- `data_loader.py`

### Submission File Naming
Name the zip file as per your ASU 10-digit ID, e.g., `1221234567.zip`.  
A different filename or submitting additional files will incur a 30-point penalty.

---

## Submission Policies

1. Late submissions will not be graded unless you have verifiable proof of an emergency. It is better to submit partial work on time for partial credit than late for no credit.
2. Each student must work independently on this exercise. High-level discussions are allowed but code-level sharing is prohibited. Plagiarism will result in failure of the course.

---

## Grading Rubric (100 pts)

### Part 1: Dockerfile & Data Loading (50 points)
- 10 pts: Docker image builds successfully without errors
- 5 pts: Working directory `/cse511/` created
- 5 pts: Java (OpenJDK 21) installed
- 5 pts: Python packages installed (`neo4j`, `pandas`, `pyarrow`)
- 15 pts: Neo4j Configuration
- 10 pts: Data Loading

### Part 2: PageRank Algorithm (25 points)
- 5 pts per test case

### Part 3: Breadth First Search (25 points)
- 5 pts per test case

---

## Testing Commands

```bash
# Build
docker build -t project1 .

# Run
docker run -d -p 7474:7474 -p 7687:7687 --name p1 project1

# Test (wait 2–4 minutes for Neo4j startup)
python3 tester.py
```

---

## Deductions

- −100 pts: Manual intervention required during build
- −100 pts: Modified template code
- −50 pts: Container doesn’t start or Neo4j service fails
- −30 pts: Incorrect filenames or extra files submitted

---

### Contents
- Introduction
- Step 0 — Exploring Graph Databases
- Step 1 — Dockerfile & Data Loading
- Step 2 — Implementing Graph Algorithms
- Grading Rubric
- Testing Commands
- Deductions
