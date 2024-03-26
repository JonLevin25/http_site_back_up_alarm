import requests
import time
import pygame
from wakepy import keep
from enum import Enum

class HTTPResponse(Enum):
    INFO = 100
    SUCCESS = 200
    REDIRECT = 300
    CLIENT_ERROR = 400
    SERVER_ERROR = 500
    WEIRD = 600

#####
### TESTING
#####

# Uncomment `TEST=True` to use google or error codes for testing

# TEST = True
test_url = "https://google.com/" # Test with google (200)
# test_url = "https://httpstat.us/500"  # Test with 500 error
# test_url = "https://httpstat.us/404"  # Test with 404 error
# test_url = "https://httpstat.us/301"  # Test with 301 redirect

#####
### CONFIG
#####
url = "https://YOUR_URL.com"
delay_between_requests = 5  # how many seconds long between receiving response and initiating next request
sound_file = "./wilhelm_scream.wav"

alarm_triggers_dict = {
    HTTPResponse.INFO: True,
    HTTPResponse.SUCCESS: True,
    HTTPResponse.REDIRECT: True,
    
    HTTPResponse.CLIENT_ERROR: False,
    HTTPResponse.SERVER_ERROR: False,
    
    HTTPResponse.WEIRD: True,
}

# TODO: Add option for non-repeating alarm sound.
# NOTE: Wakepy not tested! (but should work)


def init():
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)

def sound_the_alarm():
    print ("Press Ctrl+C to stop Alarm!! Or not...")
    # Load the audio file
    pygame.mixer.music.load(sound_file)
    
    while True:
        # Play the audio
        pygame.mixer.music.play()
        
        # This loop keeps the script running until the audio is finished playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.25)

def get_response_type(response_code):
    x = (response_code // 100) * 100
    if (x >= 100 and x < 600):
        return HTTPResponse(x)
    return HTTPResponse.WEIRD

def make_request_and_check():
    try:
        while True:
            try:
                print(f"Trying HTTP GET ({url})")
                response = requests.get(url)
                response_type = get_response_type(response.status_code)
                print(f"Response: {response_type.name} ({response.status_code})")

                should_sound_alarm = alarm_triggers_dict[response_type] 
                if should_sound_alarm:
                    print("\n\nSounding the alarm!!\n\n")
                    sound_the_alarm()
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}")
            time.sleep(delay_between_requests)  # Wait for 1 second before the next request
    except Exception as e:
        print(f"{type(e)}: {e}")
        print("An unknown script error occurred, Sounding alarm!!")
        sound_the_alarm()

if __name__ == "__main__":
    # Note: Wakelock not tested, buyt should work
    with keep.running() as wakelock: # Use keep.presnting() instead of keep.running() if you want to keep the screen on
        if not wakelock.success:
            print("Failed to acquire wakelock!!")
        try:
            if TEST:
                url = test_url
        except NameError:
            pass

        init()
        # sound_the_alarm()
        make_request_and_check()
