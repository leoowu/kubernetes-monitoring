Flags:
  -h, --help                     Show context-sensitive help (also try --help-long and --help-man).
      --web.listen-address=":9091"  
                                 Address to listen on for the web interface, API, and telemetry.
      --web.telemetry-path="/metrics"  
                                 Path under which to expose metrics.
      --web.route-prefix=""      Prefix for the internal routes of web endpoints.
      --persistence.file=""      File to persist metrics. If empty, metrics are only kept in memory.
      --persistence.interval=5m  The minimum interval at which to write out the persistence file.
      --log.level="info"         Only log messages with the given severity or above. Valid levels: [debug, info, warn, error, fatal]
      --log.format="logger:stderr"  
                                 Set the log target and format. Example: "logger:syslog?appname=bob&local=7" or "logger:stdout?json=true"
      --version                  Show application version.
