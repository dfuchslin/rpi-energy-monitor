import os
from lib.monitor import Monitor

def main():
  config = {}
  config['graphite_host'] = os.getenv('GRAPHITE_HOST')
  config['graphite_port'] = os.getenv('GRAPHITE_PORT')
  config['metric_path'] = os.getenv('METRIC_PATH')
  config['report_interval'] = os.getenv('REPORT_INTERVAL')

  try:
    monitor = Monitor(config)
    monitor.start()
  except KeyboardInterrupt:
    print("cancelling...")
  finally:
    monitor.cleanup()

main()
