import os
from lib.monitor import Monitor

def main():
  config = {}
  config['graphite_host'] = os.getenv('GRAPHITE_HOST')
  config['graphite_port'] = os.getenv('GRAPHITE_PORT')
  config['metric_prefix'] = os.getenv('METRIC_PREFIX')
  config['report_interval'] = os.getenv('REPORT_INTERVAL')
  config['prometheus_port'] = os.getenv('PROMETHEUS_PORT')

  try:
    monitor = Monitor(config)
    monitor.start()
  except KeyboardInterrupt:
    print("cancelling...")
  finally:
    monitor.cleanup()

main()
