#Author: Abhisekhar Bharadwaj Gandavarapu
#ASU ID: 1219773724

# Base image: ubuntu:22.04
FROM ubuntu:22.04

# ARGs
# https://docs.docker.com/engine/reference/builder/#understand-how-arg-and-from-interact
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# neo4j 2025.08.0 installation (match GDS v2.21.0) and some cleanup
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common && \
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y nano unzip neo4j=1:2025.08.0 python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


RUN mkdir -p /cse511
WORKDIR /cse511

RUN wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet

RUN apt-get update && \
    apt-get install -y openjdk-21-jdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

RUN pip3 install --upgrade pip && \
    pip3 install neo4j pandas pyarrow

RUN wget https://github.com/neo4j/graph-data-science/releases/download/2.21.0/neo4j-graph-data-science-2.21.0.jar -P /var/lib/neo4j/plugins/

# neo4j config
RUN echo "server.default_listen_address=0.0.0.0" >> /etc/neo4j/neo4j.conf && \
    echo "server.bolt.listen_address=0.0.0.0:7687" >> /etc/neo4j/neo4j.conf && \
    echo "server.http.listen_address=0.0.0.0:7474" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.security.procedures.unrestricted=gds.*,apoc.*" >> /etc/neo4j/neo4j.conf && \
    echo "dbms.security.procedures.allowlist=gds.*,apoc.*" >> /etc/neo4j/neo4j.conf

RUN neo4j-admin dbms set-initial-password graphprocessing

COPY data_loader.py /cse511/

# Run the data loader script
RUN chmod +x /cse511/data_loader.py && \
    neo4j start && \
    python3 data_loader.py && \
    neo4j stop

# Expose neo4j ports
EXPOSE 7474 7687

# Start neo4j service and show the logs on container run
CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]
