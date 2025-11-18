import time
import json
import random
from kafka import KafkaProducer
from faker import Faker

# Setup Kafka Producer
# Ensure your Kafka is running on localhost:9092
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda x: json.dumps(x).encode("utf-8"),
)
fake = Faker()

# CS-specific lists to randomize from
courses = [
    "Operating Systems",
    "Data Structures",
    "Web Engineering",
    "Artificial Intelligence",
    "Linear Algebra",
]
activities = ["coding", "debugging", "reading_docs", "committing_code", "running_tests"]
ides = ["VS Code", "PyCharm", "Vim", "Jupyter Notebook", "Terminal"]
errors = ["SyntaxError", "SegmentationFault", "NullPointer", "IndentationError", "None"]


def generate_student_log():
    # Select an activity first to determine if code was written
    activity = random.choice(activities)

    # Only generate lines of code if the activity is 'coding'
    loc = random.randint(5, 150) if activity == "coding" else 0

    # Only generate errors if the activity is 'debugging' or 'running_tests'
    error_type = (
        random.choice(errors) if activity in ["debugging", "running_tests"] else "None"
    )

    return {
        "timestamp": time.time(),
        "student_id": f"CS-{random.randint(2021000, 2025999)}",
        "student_name": fake.name(),
        "course": random.choice(courses),
        "activity": activity,
        "tool_used": random.choice(ides),
        "lines_of_code": loc,
        "last_error": error_type,
        "cpu_usage_pct": random.uniform(10.5, 95.0),  # Simulated local machine load
    }


if __name__ == "__main__":
    topic_name = "cs_student_logs"
    print(f"Starting producer on topic: {topic_name}...")

    try:
        while True:
            data = generate_student_log()
            producer.send(topic_name, value=data)

            # Print to console so you can see what is being generated
            print(
                f"Sent: [{data['course']}] {data['student_name']} is {data['activity']}..."
            )

            # Randomize sleep slightly to make the stream look more natural
            time.sleep(random.uniform(0.05, 0.3))

    except KeyboardInterrupt:
        print("\nStopping producer...")
        producer.close()
