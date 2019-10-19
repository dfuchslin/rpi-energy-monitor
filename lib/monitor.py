from prometheus_client import Counter, CollectorRegistry, start_http_server
from prometheus_client.bridge.graphite import GraphiteBridge
import RPi.GPIO as GPIO


class Monitor:

    def __init__(self, config):
        self.config = config
        self.sensor_gpio = self.get_config_or_default('sensor_gpio', 4)
        self.graphite_host = self.get_config_or_default('graphite_host', 'localhost')
        self.graphite_port = self.get_config_or_default('graphite_port', 2003)
        self.metric_prefix = self.get_config_or_default('metric_prefix', 'test.energy.monitor.prefix')
        self.report_interval = self.get_config_or_default('report_interval', 10)
        self.prometheus_port = self.get_config_or_default('prometheus_port', 9101)

    def get_config_or_default(self, config_param, default):
        if self.config[config_param]:
            return self.config[config_param]
        else:
            return default

    def increment(self):
        self.counter.inc()

    def start(self):
        print("Starting energy monitor:")
        print("  GPIO: {:d}".format(self.sensor_gpio))
        print("  graphite:")
        print("    server         : {}:{}".format(self.graphite_host, self.graphite_port))
        print("    metric prefix  : {}".format(self.metric_prefix))
        print("    report interval: {:d}".format(self.report_interval))
        print("  prometheus:")
        print("    port: {}".format(self.prometheus_port))
        print("    path: /metrics")

        registry = CollectorRegistry()
        self.counter = Counter('meter_power', 'Total watt-hours consumed', registry=registry)
        gb = GraphiteBridge((self.graphite_host, self.graphite_port), registry=registry)
        gb.start(self.report_interval, prefix=self.metric_prefix)
        start_http_server(self.prometheus_port, registry=registry)

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.sensor_gpio, GPIO.RISING, callback=self.increment, bouncetime=100)

    def cleanup(self):
        GPIO.cleanup()
