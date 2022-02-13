import os
import time
from lib.monitor import Monitor


def main():
    config = {}
    config['sensor_gpio'] = os.getenv('SENSOR_GPIO')
    config['graphite_enabled'] = os.getenv('GRAPHITE_ENABLED')
    config['graphite_host'] = os.getenv('GRAPHITE_HOST')
    config['graphite_port'] = os.getenv('GRAPHITE_PORT')
    config['graphite_metric_prefix'] = os.getenv('GRAPHITE_METRIC_PREFIX')
    config['graphite_report_interval'] = os.getenv('GRAPHITE_REPORT_INTERVAL')
    config['prometheus_port'] = os.getenv('PROMETHEUS_PORT')
    config['influxdb_enabled'] = os.getenv('INFLUXDB_ENABLED')
    config['influxdb_host'] = os.getenv('INFLUXDB_HOST')
    config['influxdb_port'] = os.getenv('INFLUXDB_PORT')

    try:
        monitor = Monitor(config)
        monitor.start()

        while True:
            time.sleep(60)

    except KeyboardInterrupt:
        print("cancelling...")
    finally:
        monitor.cleanup()


main()
