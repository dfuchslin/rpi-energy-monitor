from prometheus_client import start_http_server, Summary
import time

class Monitor:

  def __init__(self, config):
    self.config = config
    self.graphite_host = self.get_config_or_default('graphite_host', 'localhost')
    self.graphite_port = self.get_config_or_default('graphite_port', 2003)
    self.metric_path = self.get_config_or_default('metric_path', 'test.energy.monitor.path')
    self.report_interval = self.get_config_or_default('report_interval', 60)
    self.prometheus_port = self.get_config_or_default('prometheus_port', 9101)

  def get_config_or_default(self, config_param, default):
    if self.config[config_param]:
      return self.config[config_param]
    else:
      return default

  def start(self):
    print("Starting energy monitor:")
    print("  graphite:")
    print("    server         : {}:{}".format(self.graphite_host, self.graphite_port))
    print("    metric path    : {}".format(self.metric_path))
    print("    report interval: {:d}".format(self.report_interval))
    print("  prometheus:")
    print("    server: localhost:{}".format(self.prometheus_port))
    print("    path  : /metrics")

    start_http_server(self.prometheus_port)

    while True:
      time.sleep(1)
      print("tick tock")

  def cleanup(self):
    print("cleanup")
