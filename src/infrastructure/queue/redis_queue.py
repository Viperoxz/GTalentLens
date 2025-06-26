# src/queue/redis_queue.py
from redis import Redis
from rq import Queue

redis_conn = Redis(host='localhost', port=6379)
cv_queue = Queue("cv_tasks", connection=redis_conn)
entity_queue = Queue("entity_tasks", connection=redis_conn)
