# PostgreSQL failover runbook

This operational runbook explains how to trigger manual database failover during primary node degradation.

## Scope and routing

Follow these instructions when the primary database node stops accepting write traffic.

## Emergency failover procedure

WARNING: Verify that the secondary node replication lag is zero before you promote the node. Promoting a lagging node causes data loss.

1. Check the replication status on the standby replica:
   ```bash
   pg_stat_replication --host=standby.internal
   ```
2. Verify that `byte_lag` equals `0`.
3. Stop the active primary service:
   ```bash
   systemctl stop postgresql@primary
   ```
4. Promote the standby node to primary:
   ```bash
   pg_ctl promote -D /var/lib/postgresql/data
   ```
5. Update DNS pointer `db.internal` to the promoted node IP address.
6. Verify that applications write successfully to the promoted database.
