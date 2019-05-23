import Adafruit_PCA9685
import time
import random

PWM_FREQ = 60

pca = Adafruit_PCA9685.PCA9685()
pca.set_pwm_freq(PWM_FREQ)

def pwm(ms):
    value = ms / 1000 / (1/PWM_FREQ) * 4096
    pca.set_pwm(0,0,int(value))

def sweepto(current, target, step=25, pause=.01):
    current_us = int(current * 1000)
    target_us = int(target * 1000)
    direction = step if target > current else -step
    sweepvals_us = list(range(current_us, target_us, direction))
    sweepvals_us.append(target_us)
    for current in sweepvals_us:
        pwm(current / 1000)
        time.sleep(pause)
    return target


def dance(duration):
    # To catch in the servo, we sweep the whole range with reduced speed
    sweepto(1,2,step=5)
    sweepto(2,1,step=5)
    sweepto(1,2,step=5)
    # Then, go to middle position
    sweepto(2,1.5)
    # And dance
    start = time.time()
    current = 1.5
    while time.time() - start < duration:
        current = sweepto(current, 1+random.random())
        print(current)
        time.sleep(.2)

if __name__ == "__main__":
    dance(3)
