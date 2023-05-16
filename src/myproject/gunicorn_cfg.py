import gevent
import psycogreen.gevent

bind = "0.0.0.0:5000"
forwarded_allow_ips = "*"
timeout = 180
worker_class = "gevent"
workers = 5  # a better way: multiprocessing.cpu_count() * 2 + 1


def post_fork(server, worker):
    gevent.monkey.patch_all()
    psycogreen.gevent.patch_psycopg()
