/prometheus $ /bin/prometheus --help
usage: prometheus [<flags>]

The Prometheus monitoring server

Flags:
  -h, --help                     Show context-sensitive help (also try --help-long and --help-man).
      --version                  Show application version.
      --config.file="prometheus.yml"  
                                 Prometheus configuration file path.
      --web.listen-address="0.0.0.0:9090"  
                                 Address to listen on for UI, API, and telemetry.
      --web.read-timeout=5m      Maximum duration before timing out read of the request, and closing idle connections.
      --web.max-connections=512  Maximum number of simultaneous connections.
      --web.external-url=<URL>   The URL under which Prometheus is externally reachable (for example, if Prometheus is served via a reverse proxy). Used for generating relative and absolute links back to Prometheus itself. If the URL
                                 has a path portion, it will be used to prefix all HTTP endpoints served by Prometheus. If omitted, relevant URL components will be derived automatically.
      --web.route-prefix=<path>  Prefix for the internal routes of web endpoints. Defaults to path of --web.external-url.
      --web.user-assets=<path>   Path to static asset directory, available at /user.
      --web.enable-lifecycle     Enable shutdown and reload via HTTP request.
      --web.enable-admin-api     Enable API endpoints for admin control actions.
      --web.console.templates="consoles"  
                                 Path to the console template directory, available at /consoles.
      --web.console.libraries="console_libraries"  
                                 Path to the console library directory.
      --storage.tsdb.path="data/"  
                                 Base path for metrics storage.
      --storage.tsdb.retention=15d  
                                 How long to retain samples in storage.
      --storage.tsdb.no-lockfile  
                                 Do not create lockfile in data directory.
      --storage.remote.flush-deadline=<duration>  
                                 How long to wait flushing sample on shutdown or config reload.
      --alertmanager.notification-queue-capacity=10000  
                                 The capacity of the queue for pending Alertmanager notifications.
      --alertmanager.timeout=10s  
                                 Timeout for sending alerts to Alertmanager.
      --query.lookback-delta=5m  The delta difference allowed for retrieving metrics during expression evaluations.
      --query.timeout=2m         Maximum time a query may take before being aborted.
      --query.max-concurrency=20  
                                 Maximum number of queries executed concurrently.
      --log.level=info           Only log messages with the given severity or above. One of: [debug, info, warn, error]
