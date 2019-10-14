import time

class Monitor:

  def __init__(self, config):
    self.graphite_host = config['graphite_host']
    self.graphite_port = config['graphite_port']
    self.metric_path = config['metric_path']
    self.report_interval = config['report_interval']

  def start(self):
    print("start")
    while True:
      time.sleep(1)
      print("tick tock")

  def cleanup(self):
    print("cleanup")
