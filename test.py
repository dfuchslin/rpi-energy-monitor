import time, random
import RPi.GPIO as GPIO

total_count = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def my_callback(channel):
  global total_count
  print(" --> measured pulse")
  total_count += 1

GPIO.add_event_detect(4, GPIO.RISING, callback=my_callback, bouncetime=100)

def go():
  global total_count
  starttime = time.time()
  interval = 10.0

  while True:
    print("total_count={:d}".format(total_count))
    time.sleep(random.uniform(0,5))
    time.sleep(interval - ((time.time() - starttime) % interval))


try:
  print("starting...")
  go()
except KeyboardInterrupt:
  GPIO.cleanup()
GPIO.cleanup()
