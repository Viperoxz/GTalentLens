# src/infrastructure/queue/redis_queue.py
from redis import Redis, ConnectionError
from rq import Queue
import time

def wait_for_redis(host, port, retries=5, delay=2):
    for i in range(retries):
        try:
            conn = Redis(host=host, port=port)
            conn.ping()
            return conn
        except ConnectionError:
            print(f"[Retry {i+1}] Redis chưa sẵn sàng, thử lại sau {delay}s...")
            time.sleep(delay)
    raise Exception("Không thể kết nối Redis sau nhiều lần thử.")

redis_conn = wait_for_redis("redis", 6379)
cv_queue = Queue("cv_tasks", connection=redis_conn)
entity_queue = Queue("entity_tasks", connection=redis_conn)
