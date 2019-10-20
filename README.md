# rpi-energy-monitor

Python application to detect pulses from the utility meter LED using a pulse sensor.https://shop.openenergymonitor.com/optical-utility-meter-led-pulse-sensor/

The script counts the number of pulses and sends the data to a Graphite server and also exposes a Prometheus metrics endpoint for scraping.

## Dependencies:

    apt install python3-rpi.gpio
    pip3 install prometheus_client

## Pulse sensor configuration:

  | Sensor pin | Rpi pin   |
  |------------|-----------|
  | 2          | 1 (3V3)   |
  | 5          | 3 (GND)   |
  | 6          | 7 (GPIO4) |

## Script options:

  | environment variable       | description                                    | default     |
  |----------------------------|------------------------------------------------|-------------|
  | `SENSOR_GPIO`              | Rpi GPIO channel to which sensor is connected  | 4           |
  | `GRAPHITE_HOST`            | Graphite server hostname/ip                    | localhost   |
  | `GRAPHITE_PORT`            | Graphite server port                           | 2003        |
  | `GRAPHITE_METRIC_PREFIX`   | Graphite metric path prefix                    | test.prefix |
  | `GRAPHITE_REPORT_INTERVAL` | Graphite reporting interval, in seconds        | 10          |
  | `PROMETHEUS_PORT`          | Port on localhost to serve Prometheus metrics  | 9101        |
