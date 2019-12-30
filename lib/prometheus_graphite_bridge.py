import requests
import time
import re
import socket
from datetime import datetime

class PrometheusToGraphiteMetricConverterBridge:

    def __init__(self, config):
        self.config = config
        self.prometheus_url = self.get_config_or_default('prometheus_url', 'http://localhost:9100/metrics')
        self.prometheus_metric = self.get_config_or_default('prometheus_metric', 'meter_power_total')
        self.prometheus_poll_interval = int(self.get_config_or_default('prometheus_poll_interval', 10))
        self.graphite_host = self.get_config_or_default('graphite_host', 'localhost')
        self.graphite_port = int(self.get_config_or_default('graphite_port', 2003))
        self.graphite_metric = self.get_config_or_default('graphite_metric', 'test.metric')
        self.prometheus_regex = re.compile(f"^{self.prometheus_metric} ([0-9.]+)", re.MULTILINE)

    def get_config_or_default(self, config_param, default):
        if self.config[config_param]:
            return self.config[config_param]
        else:
            return default

    def start(self):
        print("Starting energy monitor bridge:")
        print("  prometheus:")
        print("    url           : {}".format(self.prometheus_url))
        print("    metric        : {}".format(self.prometheus_metric))
        print("    poll interval : {}".format(self.prometheus_poll_interval))
        print("  graphite:")
        print("    server        : {}:{}".format(self.graphite_host, self.graphite_port))
        print("    metric        : {}".format(self.graphite_metric))

        previous_metric = self.create_metric(0, -1)
        while(True):
            loop_start_time = self.now()
            current_metric = self.calculate_current_metric(previous_metric)
            if current_metric['timestamp'] == previous_metric['timestamp']:
                print(f"Metric not updated: {current_metric}")
            else:
                if self.send_metric(current_metric):
                    previous_metric = current_metric
            loop_execution_time = self.now() - loop_start_time
            sleep_time = self.prometheus_poll_interval - loop_execution_time.total_seconds()
            time.sleep(max(sleep_time, 0))

    def now(self):
        return datetime.now()

    def create_metric(self, total, value):
        result = {}
        result['timestamp'] = self.now()
        result['total'] = int(total)
        result['value'] = int(value)
        return result

    def calculate_current_metric(self, previous_metric):
        result = previous_metric
        try:
            response = requests.get(self.prometheus_url, timeout=self.prometheus_poll_interval)
            response.raise_for_status()
            m = self.prometheus_regex.search(response.text)
            if m is None:
                raise Exception(f"'{self.prometheus_metric}' not found in response!")
            current_total = int(float(m.group(1)))
            previous_total = previous_metric['total']
            current_value = max(current_total - previous_total, 0)
            # first request should not be sent, record current_total for the next calculation
            if result['value'] < 0:
                result['total'] = current_total
                result['value'] = current_value
            else:
                result = self.create_metric(current_total, current_value)
        except Exception as e:
            print(f"Could not get metric from prometheus: {e}")
        finally:
            return result

    def send_metric(self, current_metric):
        try:
            timestamp = int(datetime.timestamp(datetime.utcnow()))
            msg = "{} {:0.0f} {:d}\n".format(self.graphite_metric, current_metric['value'], timestamp)
            print("importing to {}:{}  [{}]".format(self.graphite_host, self.graphite_port, msg.replace('\n', '')), flush=True)
            sock = socket.socket()
            sock.connect((self.graphite_host, self.graphite_port))
            sock.sendall(msg.encode())
            sock.close()
            return True
        except Exception as e:
            print(f"Problem sending metric to graphite: {e}")
            return False

    def cleanup(self):
        print("cleanup")
