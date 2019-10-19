import os
import time
from lib.monitor import Monitor


def main():
    config = {}
    config['sensor_gpio'] = os.getenv('SENSOR_GPIO')
    config['graphite_host'] = os.getenv('GRAPHITE_HOST')
    config['graphite_port'] = os.getenv('GRAPHITE_PORT')
    config['metric_prefix'] = os.getenv('METRIC_PREFIX')
    config['report_interval'] = os.getenv('REPORT_INTERVAL')
    config['prometheus_port'] = os.getenv('PROMETHEUS_PORT')

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
