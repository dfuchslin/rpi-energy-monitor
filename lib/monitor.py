from prometheus_client import Counter, CollectorRegistry, start_http_server
from prometheus_client.bridge.graphite import GraphiteBridge
from distutils.util import strtobool
import RPi.GPIO as GPIO


class Monitor:

    def __init__(self, config):
        self.config = config
        self.sensor_gpio = int(self.get_config_or_default('sensor_gpio', 4))
        self.graphite_enabled = self.get_config_or_default_bool('graphite_enabled', True)
        self.graphite_host = self.get_config_or_default('graphite_host', 'localhost')
        self.graphite_port = int(self.get_config_or_default('graphite_port', 2003))
        self.graphite_metric_prefix = self.get_config_or_default('graphite_metric_prefix', 'test.prefix')
        self.graphite_report_interval = int(self.get_config_or_default('graphite_report_interval', 10))
        self.prometheus_port = int(self.get_config_or_default('prometheus_port', 9101))
        self.influxdb_enabled = self.get_config_or_default_bool('influxdb_enabled', True)
        self.influxdb_host = self.get_config_or_default('influxdb_host', 'localhost')
        self.influxdb_port = int(self.get_config_or_default('influxdb_port', 12003))

    def get_config_or_default(self, config_param, default):
        if self.config[config_param]:
            return self.config[config_param]
        else:
            return default

    def get_config_or_default_bool(self, config_param, default):
        val = self.config[config_param]
        if val is not None:
            return bool(strtobool(val))
        else:
            return default

    def increment(self, channel):
        self.counter.inc()

    def start(self):
        print("Starting energy monitor:")
        print("  GPIO: {:d}".format(self.sensor_gpio))
        print("  graphite:")
        print("    enabled        : {}".format(self.graphite_enabled))
        print("    server         : {}:{}".format(self.graphite_host, self.graphite_port))
        print("    metric prefix  : {}".format(self.graphite_metric_prefix))
        print("    report interval: {:d}".format(self.graphite_report_interval))
        print("  influxdb (graphite protocol):")
        print("    enabled        : {}".format(self.influxdb_enabled))
        print("    server         : {}:{}".format(self.influxdb_host, self.influxdb_port))
        print("    metric prefix  : {}".format(self.graphite_metric_prefix))
        print("    report interval: {:d}".format(self.graphite_report_interval))
        print("  prometheus:")
        print("    port: {}".format(self.prometheus_port))
        print("    path: /metrics")

        registry = CollectorRegistry()
        self.counter = Counter('meter_power', 'Total watt-hours consumed', registry=registry)
        if self.graphite_enabled:
            gb = GraphiteBridge((self.graphite_host, self.graphite_port), registry=registry)
            gb.start(self.graphite_report_interval, prefix=self.graphite_metric_prefix)
        if self.influxdb_enabled:
            influxbridge = GraphiteBridge((self.influxdb_host, self.influxdb_port), registry=registry)
            influxbridge.start(self.graphite_report_interval, prefix=self.graphite_metric_prefix)
        start_http_server(self.prometheus_port, registry=registry)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_gpio, GPIO.RISING, callback=self.increment, bouncetime=100)

    def cleanup(self):
        GPIO.cleanup()
