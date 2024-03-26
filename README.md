HTTP Alarm
============

A simple script to poll a website with HTTP requests, playing an alarm whenever it returns a valid response.

## Requirements
* Python 3

```
pip install requirements.txt
```

## Usage
* Adjust paramaters in config section
* Test by uncommenting `TEST = True`
* Run with `python http_tester_alarm.py`, keep running.
* Alarm sound will play on repeat when server returns valid response.