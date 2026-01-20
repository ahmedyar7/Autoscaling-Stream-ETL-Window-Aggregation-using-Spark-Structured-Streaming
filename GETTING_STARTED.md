# Getting Started - Execution Guide

This guide walks you through running the Autoscaling Stream ETL project step-by-step.

## Prerequisites

Before starting, ensure you have completed all prerequisites from the [main README](README.md#prerequisites-windows-environment):

- Docker Desktop
- Apache Spark (4.0.1 or 3.5.x)
- Python 3.14+ with uv
- Java JDK (17 or 11)
- Windows: `hadoop.dll` in `C:\Windows\System32`

### Install Project Dependencies

```powershell
# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Or sync all dependencies
uv sync
```

---

## Step-by-Step Execution

Follow these steps in **PowerShell** to replicate the autoscaling demo. You'll need **5 separate terminal windows**.

### Step 1: Start the Messaging Queue (Kafka)

**Terminal 1**

Start the Docker container for Kafka.

```powershell
docker-compose up -d
```

This starts the Kafka broker on `localhost:9092`.

---

### Step 2: Start the Spark Master

**Terminal 2**

Open a new PowerShell terminal and launch the Master node.

```powershell
spark-class org.apache.spark.deploy.master.Master
```

**Important Notes:**
- Copy the **Master URL** from the logs (e.g., `spark://192.168.100.110:7077`)
- Open a browser and go to `http://localhost:8081` to access the Spark Master Dashboard
- You'll need this URL for the next step

---

### Step 3: Start the Spark Worker

**Terminal 3**

Open a new PowerShell terminal and connect a worker to the Master.

```powershell
# Replace 192.168.100.110 with YOUR Master IP from Step 2
spark-class org.apache.spark.deploy.worker.Worker spark://192.168.100.110:7077
```

You should see a confirmation message that the worker registered with the master.

---

### Step 4: Start the Data Producer

**Terminal 4**

Open a new PowerShell terminal. This script generates simulated student activity logs continuously.

```powershell
python producer.py
```

You should see messages being published to the Kafka topic `cs_student_logs`. The logs will look like:
```
Publishing: {"timestamp": 1234567890.123, "student_name": "Ahmed Yar", ...}
```

---

### Step 5: Submit the Streaming Job

**Terminal 5**

Open a new PowerShell terminal and submit the Spark Streaming job.

```powershell
spark-submit `
  --master spark://192.168.100.110:7077 `
  --executor-cores 2 `
  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 `
  --conf spark.dynamicAllocation.enabled=true `
  --conf spark.dynamicAllocation.minExecutors=0 `
  --conf spark.dynamicAllocation.maxExecutors=4 `
  --conf spark.dynamicAllocation.executorIdleTimeout=10s `
  --conf spark.dynamicAllocation.schedulerBacklogTimeout=1s `
  stream_job.py
```

**Alternative (single-line):**
```powershell
spark-submit --master spark://192.168.100.110:7077 --executor-cores 2 --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1 --conf spark.dynamicAllocation.enabled=true --conf spark.dynamicAllocation.minExecutors=0 --conf spark.dynamicAllocation.maxExecutors=4 --conf spark.dynamicAllocation.executorIdleTimeout=10s --conf spark.dynamicAllocation.schedulerBacklogTimeout=1s stream_job.py
```

The job will start processing messages from Kafka and performing window aggregations. You should see output in the console showing processed records.

---

## Demonstrating Autoscaling

Once the system is running and processing data, follow these steps to observe the cluster scaling:

### Phase 1: Verify Baseline

1. Go to `http://localhost:8081` in your browser (Spark Master UI)
2. Click on your running application
3. Click the **Executors** tab
4. You should see **1 Active Executor** processing the baseline load

### Phase 2: Create a Traffic Spike

1. Open **3-4 additional PowerShell terminals** (besides the one running producer.py)
2. In each new terminal, run:
   ```powershell
   python producer.py
   ```
3. You now have 4 concurrent producer instances flooding the system with data

### Phase 3: Observe Autoscaling (Scaling Out)

1. Refresh the **Executors** tab in the Spark UI
2. Within seconds, you'll see new executors being launched:
   - Executor 2 appears
   - Executor 3 appears
   - Executor 4 appears

**Why?** Spark's dynamic allocation detected the message backlog in Kafka and automatically scaled the cluster from 1 to 4 executors to handle the load.

### Phase 4: Observe Cooldown (Scaling In)

1. Close all the extra producer terminals (keep one running if you want)
2. Wait approximately **15 seconds** for the system to cool down
3. Refresh the **Executors** tab
4. Executors 2, 3, and 4 will be killed, leaving only **1 Active Executor**

**Why?** Once the backlog is cleared and no new messages arrive, Spark realizes the extra executors are idle and removes them to save resources.

---

## Troubleshooting

### Kafka Connection Issues
- Ensure Docker is running: `docker ps`
- Check if Kafka container is running: `docker-compose ps`
- Verify broker is accessible: `netstat -an | findstr 9092` (Windows)

### Spark Master Not Starting
- Make sure Java is installed and in PATH: `java -version`
- Check firewall settings aren't blocking port 7077
- Look for error messages in the terminal output

### Producer Not Sending Data
- Verify Kafka is running on `localhost:9092`
- Check for Python import errors: ensure `kafka-python` is installed (`uv sync`)
- Try running with verbose output: `python -u producer.py`

### Stream Job Not Processing
- Replace `192.168.100.110` with your actual machine IP
- Ensure the Spark Worker is connected to the Master (visible in Master UI)
- Check console output for error messages
- Verify Kafka topic `cs_student_logs` exists (producer creates it)

---

## Stopping the System

To cleanly shut down all components:

1. **Ctrl+C** on each terminal running producer, streaming job, worker, and master
2. Stop Kafka and dependencies:
   ```powershell
   docker-compose down
   ```

---

## Next Steps

- Review the [project report](./assets/Final%20Project%20Report.pdf) for theoretical details
- Examine [producer.py](producer.py) to understand data generation
- Examine [stream_job.py](stream_job.py) to understand the ETL pipeline
- Modify scaling parameters in the spark-submit command to experiment with different configurations
