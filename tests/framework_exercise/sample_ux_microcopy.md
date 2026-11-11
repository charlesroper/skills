# Interface and CLI microcopy

This catalogue specifies button labels, error recovery messages and empty states for the deployment console.

## Component specifications

### Error messages

- **Database write timeout:** Cannot save deployment configuration (socket timeout after 30 seconds). Check network connection and retry the save operation.
- **Permission denied:** Cannot overwrite `/etc/app/config.json` (permission denied). Run command again with elevated privileges or specify a user directory with `--config`.

### Action buttons and confirmation dialogs

- **Dialog title:** Delete deployment cluster?
- **Primary action:** Delete cluster
- **Secondary action:** Keep cluster

### Empty state

- **Title:** No deployment environments yet
- **Description:** Create your first deployment environment to configure staging and production pipelines.
- **Action button:** Create environment
