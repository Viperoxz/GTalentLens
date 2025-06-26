import os
from redis import Redis, ConnectionError
from rq import Queue
import time
from dotenv import load_dotenv

load_dotenv()

def wait_for_redis(host, port, retries=5, delay=2):
    for i in range(retries):
        try:
            conn = Redis(host=host, port=port)
            conn.ping()
            return conn
        except ConnectionError:
            print(f"[Retry {i+1}] Redis not ready yet, please try again {delay}s...")
            time.sleep(delay)
    raise Exception("Cannot connect Redis after multiple tries.")

# Detect environment
REDIS_HOST = os.getenv("REDIS_HOST", "redis")

redis_conn = wait_for_redis(REDIS_HOST, 6379)
cv_queue = Queue("cv_tasks", connection=redis_conn)
entity_queue = Queue("entity_tasks", connection=redis_conn)
