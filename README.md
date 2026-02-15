<div align="center">
    <img src="./assets/font-page.png" />
</div>

<!-- <h1 align="center">
Autoscaling Stream ETL & Window Aggregation using Spark Structured Streaming
</h1>

<div style="text-align:center">
    <img src="https://img.shields.io/badge/Apache%20Spark-4.0.1-E25A1C?style=flat&logo=apachespark&logoColor=white" alt="Apache Spark" style="margin:0 6px;vertical-align:middle"/>
    <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white" alt="Python" style="margin:0 6px;vertical-align:middle"/>
    <img src="https://img.shields.io/badge/Apache%20Kafka-Latest-231F20?style=flat&logo=apachekafka&logoColor=white" alt="Kafka" style="margin:0 6px;vertical-align:middle"/>
    <img src="https://img.shields.io/badge/Docker-Required-2496ED?style=flat&logo=docker&logoColor=white" alt="Docker" style="margin:0 6px;vertical-align:middle"/>
    <img src="https://img.shields.io/badge/Java-11%20%7C%2017-007396?style=flat&logo=openjdk&logoColor=white" alt="Java" style="margin:0 6px;vertical-align:middle"/>
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat" alt="License" style="margin:0 6px;vertical-align:middle"/>
    <img src="https://img.shields.io/badge/Status-Active-success?style=flat" alt="Status" style="margin:0 6px;vertical-align:middle"/>
</div>

<br/>
 -->


--- 

## Project Overview

This project demonstrates a **Cloud-Native Autoscaling Data Pipeline**. It simulates a real-time stream of Computer Science student activity logs, processes them using **Apache Spark Structured Streaming**, and dynamically scales computing resources based on traffic load.

### Key Features

1.  **Real-Time ETL:** Ingests raw logs from Kafka, parses JSON, and filters data.
2.  **Window Aggregation:** Calculates "Total Lines of Code" and "Average CPU Usage" over sliding 10-second windows.
3.  **Dynamic Autoscaling:** The cluster automatically scales from **0 to 4 Executors** based on incoming load (Backlog).
4.  **Resource Optimization:** configured to prevent resource hoarding (limits executors to 2 cores each).

---

## Architecture

```mermaid
flowchart TD
    %% Accessible Muted Color Palette
    classDef source fill:#E3F2FD,stroke:#1565C0,stroke-width:2px,color:#0D47A1
    classDef ingest fill:#F5F5F5,stroke:#424242,stroke-width:2px,color:#212121
    classDef master fill:#FFF3E0,stroke:#E65100,stroke-width:2px,color:#BF360C
    classDef worker fill:#FFFFFF,stroke:#757575,stroke-width:1px,color:#424242
    classDef serve fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px,color:#1B5E20

    %% Nodes
    DS["<b>Data Source</b><br/>Python Producer (Faker)"]:::source
    IL["<b>Ingestion Layer</b><br/>Apache Kafka (Topic: logs)"]:::ingest

    subgraph Cluster ["Processing Layer (Spark Cluster)"]
        direction TB
        SM["<b>Spark Master</b><br/>Driver / Scheduler"]:::master
        
        %% Workers
        W1["Worker 1<br/>(Active)"]:::worker
        W2["Worker 2<br/>(Active)"]:::worker
        WN["Worker N<br/>(Dynamic)"]:::worker
        
        %% Internal Structure
        SM --- W1
        SM --- W2
        SM --- WN
    end

    SL["<b>Serving Layer</b><br/>Console Output / Dashboard"]:::serve

    %% Data Flow Connections
    DS --> IL
    IL --> SM
    
    %% Output flow from workers to serving
    W1 & W2 & WN --> SL

    %% Subgraph Box Styling (Soft Gray)
    style Cluster fill:#FAFAFA,stroke:#BDBDBD,stroke-dasharray: 5 5
    style WN stroke-dasharray: 4 4
```

<!-- <div>
    <img src="./assets/system-design.png">
</div> -->

---

## Project Demo
<div align="center">
    <a href="https://drive.google.com/file/d/16rk1fZsm3CFEdXcpfkzRPgar77e3Q5Oe/view?usp=sharing">
        <img src="./assets/thumbnail.png" />
    </a>
</div>
---


## Prerequisites (Windows Environment)

To run this project locally, ensure you have the following installed:

1.  **Docker Desktop** (For running Apache Kafka).
2.  **Apache Spark** (Version 4.0.1 or 3.5.x).
3.  **Python 3.14+** (with `uv` package manager for dependency management).
4.  **Java JDK** (Version 17 or 11).
5.  **CRITICAL:** `hadoop.dll` must be present in your `C:\Windows\System32` folder or your Hadoop bin folder to fix Windows file permission errors.
6.  **uv** (Fast Python package manager) - [Install uv](https://docs.astral.sh/uv/getting-started/)

### Install Project Dependencies with uv

This project uses `uv` for fast, reliable dependency management. After cloning the repository:

```powershell
# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Or install all dependencies at once
uv sync
```

The project dependencies are defined in `pyproject.toml`:
- **pyspark** (4.1.1+) - Apache Spark for distributed stream processing
- **kafka-python** (2.3.0+) - Kafka client for message publishing
- **faker** (40.1.2+) - Fake data generation for testing

---

## Getting Started

Ready to run the project? Follow the comprehensive step-by-step guide in [**GETTING_STARTED.md**](GETTING_STARTED.md) which includes:

- Detailed setup instructions
- 5-terminal execution walkthrough
- How to demonstrate autoscaling in action
- Troubleshooting tips
- System shutdown procedures

---

<div align="">
  <h3>📄 Full Project Report</h3>
  <p>For a deep dive into the theoretical concepts, cost analysis, and implementation details, please view the academic report.</p>
  <a href="./assets/Final Project Report.pdf">
    <img src="https://img.shields.io/badge/Read%20PDF-Project%20Report-blue?styleflat=for-the-badge&logo=adobeacrobatreader" alt="Read Report">
  </a>
</div>
