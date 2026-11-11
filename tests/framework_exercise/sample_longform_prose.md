# Rebuilding the sync daemon

At dawn on 18 October, our distributed synchronisation daemon deadlocked during peak export traffic. That failure taught us that coordination clusters often create more operational friction than the concurrency problems they claim to solve.

We began with three nodes managing distributed locks across ten background worker queues. Whenever network latency spiked between data centres, heartbeat timeouts triggered false leader re-elections. Each re-election stalled active exports and queued thousands of retries behind exhausted connection pools.

We decided to strip the cluster entirely. We replaced distributed locking with single-writer SQLite databases on local NVMe drives – a pattern known as write-ahead replication. Throughput doubled within an hour. Our incident pager has remained quiet ever since.
