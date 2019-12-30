import os
import time
from lib.prometheus_graphite_bridge import PrometheusToGraphiteMetricConverterBridge


def main():
    config = {}
    config['prometheus_url'] = os.getenv('PROMETHEUS_URL')
    config['prometheus_metric'] = os.getenv('PROMETHEUS_METRIC')
    config['prometheus_poll_interval'] = os.getenv('PROMETHEUS_POLL_INTERVAL')
    config['graphite_host'] = os.getenv('GRAPHITE_HOST')
    config['graphite_port'] = os.getenv('GRAPHITE_PORT')
    config['graphite_metric'] = os.getenv('GRAPHITE_METRIC')

    try:
        bridge = PrometheusToGraphiteMetricConverterBridge(config)
        bridge.start()
    except KeyboardInterrupt:
        print("cancelling...")
    finally:
        bridge.cleanup()


main()
