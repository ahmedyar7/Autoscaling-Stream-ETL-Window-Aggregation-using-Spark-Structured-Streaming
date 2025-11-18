# Autoscaling Stream ETL & Window Aggregation using Spark Structured Streaming

## 💻 Project Title

**Autoscaling Stream ETL & Window Aggregation using Spark Structured Streaming**

## 💡 Overview

This project implements a complete, real-time data pipeline designed to demonstrate the elasticity of **Apache Spark Structured Streaming** using **Dynamic Allocation**.

The pipeline simulates logging activity from Computer Science students, performs windowed aggregation (calculating total lines of code and average CPU usage), and automatically scales the number of Spark executors in response to varying data ingestion rates (simulated load spikes).

## 🚀 Deliverables Implemented

| Deliverable | Description | Status |
| :--- | :--- | :--- |
| **Spark Streaming Job** | PySpark script (`stream_job.py`) with Kafka source, ETL, Watermarking, and Window Aggregation. | ✅ Implemented |
| **Dynamic Allocation** | Spark configuration for automatic scaling (min 0, max 4 executors). | ✅ Configured |
| **Load Simulation** | Python script (`producer.py`) to simulate variable load spikes in Kafka. | ✅ Implemented |
| **Sink** | Console sink for real-time visualization of results. | ✅ Implemented |

---

## 🛠️ Phase 1: Environment Setup (Windows)

This project requires **Docker** (for Kafka), a local **Apache Spark** installation (with Java), and **winutils.exe** properly configured.

### A. Kafka Setup (via Docker)

1.  **Prerequisites:** Ensure **Docker Desktop** is running and functional.
2.  **Start Kafka:** Navigate to the folder containing your `docker-compose.yml` file and run:
    ```bash
    docker-compose up -d
    ```
    *This starts the Zookeeper and Kafka broker containers on `localhost:9092`.*

### B. Spark Standalone Cluster Setup

To demonstrate autoscaling, you must manually launch the Master and Worker nodes.

1.  **Start Spark Master (CMD 1):**
    Navigate to your Spark installation's `bin` folder (e.g., `C:\spark...\bin`).

    ```bash
    spark-class org.apache.spark.deploy.master.Master
    ```

    *Observation: Note the Master URL displayed (e.g., `spark://<YOUR-IP>:7077`).*

2.  **Start Spark Worker (CMD 2):**
    Open a **new** terminal, navigate to the Spark `bin` folder, and use the Master URL:

    ```bash
    spark-class org.apache.spark.deploy.worker.Worker spark://<YOUR-IP>:7077
    ```

---

## ⚙️ Phase 2: Execution and Demonstration

### A. Start the Kafka Producer (`producer.py`)

The producer sends simulated student activity data to the `cs_student_logs` topic.

1.  **Activate Virtual Environment** (Recommended Best Practice):
    ```bash
    .\.venv\Scripts\activate
    ```
2.  **Install Python Dependencies:**
    ```bash
    pip install kafka-python faker
    ```
3.  **Run the Producer (CMD 3):**
    ```bash
    python producer.py
    ```
    *Troubleshooting:* If you receive a `ModuleNotFoundError` after installation, use the full path to your global Python installation: `D:\Python 3.13\python.exe producer.py`.
    *Observation: The terminal will show continuous log lines being sent.* **(Keep this running.)**

### B. Submit the Streaming Job (`stream_job.py`)

This command launches the ETL job on your local Spark cluster with dynamic allocation enabled.

1.  **Open a NEW Terminal (CMD 4)** and navigate to the folder containing `stream_job.py`.
2.  **Submit the Job:** Ensure you replace `<YOUR-IP>` with the actual Master IP.
    ```bash
    spark-submit ^
    --master spark://<YOUR-IP>:7077 ^
    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0 ^
    --conf spark.dynamicAllocation.enabled=true ^
    --conf spark.dynamicAllocation.minExecutors=0 ^
    --conf spark.dynamicAllocation.maxExecutors=4 ^
    --conf spark.dynamicAllocation.executorIdleTimeout=10s ^
    --conf spark.dynamicAllocation.schedulerBacklogTimeout=1s ^
    stream_job.py
    ```
    *Note: If running on Linux/macOS, replace the line continuation character `^` with `\`.
    *Observation: This terminal will start printing the Window Aggregation results (Total LOC, Avg CPU) every 5 seconds.*

---

## 📈 Phase 3: Demonstration of Autoscaling

### A. Observe Scaling UP

1.  **Monitor the Spark UI:** Open the Application UI at **`http://localhost:4040`**. Navigate to the **Executors** tab.
2.  **Initial State:** You should see 0 or 1 active executor.
3.  **Simulate Load Spike:** Open **two (2) or three (3) additional** terminals and run the producer script in each one simultaneously.
    ```bash
    python producer.py
    ```
4.  **Verification:** Watch the **Executors** tab. The number should rapidly increase towards the `maxExecutors=4` limit as Spark requests resources to handle the increased load.

### B. Observe Scaling DOWN

1.  **Stop the Load:** Close the extra producer terminals (leaving only the initial one running).
2.  **Verification:** After the backlog is cleared, the executors will become idle. Due to `executorIdleTimeout=10s`, Spark will automatically terminate them, scaling the cluster back down to the minimum size.

---

## 📊 Evaluation Metrics

To satisfy the project requirements, gather the following metrics from the **Spark UI** during the scaling test:

1.  **Throughput/Latency:** In the **Structured Streaming** tab, record the "Input Rate" vs. "Process Rate" before, during, and after the spike.
2.  **Resource Utilization:** Record the total number of Active Executors over time as the load changes.