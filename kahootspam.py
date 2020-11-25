from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions

from time import sleep
import sys, random
import threading

if len(sys.argv) != 3:
    gamepin = input('Game PIN: ')
    numofthreads = int(input('# of bots: '))
    name = input("Nickname: ")
else:
    numofthreads = int(sys.argv[2])
    gamepin = sys.argv[1]


options = ChromeOptions()
options.add_argument('headless')
driver_count = 0
pin_count = 0
username_count = 0
done_count = 0

def new_game(i):
    """Launches a new kahoot login with selenium
    new_game(<number to display on error>)"""
    global driver_count, pin_count, username_count, done_count
    driver = Chrome(ChromeDriverManager().install(), chrome_options=options)
    driver.get('https://kahoot.it/')
    driver_count += 1
    try:
        pinning = driver.find_element_by_xpath('//*[@id="game-input"]')
        pinning.send_keys(gamepin)
        pinning.send_keys(Keys.ENTER)
        pin_count += 1
        sleep(1)
        nick = driver.find_element_by_xpath(
            '//*[@id="nickname"]')
        username_count += 1
        nick.send_keys(name + str(username_count))
        nick.send_keys(Keys.ENTER)
        done_count += 1
    except TypeError:
        print("Thread #%i has errored!" % i)

def spawn(numofthreads):
    threads = []
    for i in range(numofthreads):
        threads.append(threading.Thread(target=new_game, args=[i]))
        threads[-1].start()
        print("\r[%i/%i] Starting threads" % (i+1, numofthreads), end='')

spawn(numofthreads)
print()

while driver_count < numofthreads:
    print("\r[%i/%i] Starting webdriver" % (driver_count, numofthreads), end='')
while pin_count < numofthreads:
    print("\r[%i/%i] Entering game pin." % (pin_count, numofthreads), end='')
while username_count < numofthreads:
    print("\r[%i/%i] Entering in nickname" % (username_count, numofthreads), end='')
while done_count < numofthreads:
    print("\r%i/%i threads done.      " % (done_count, numofthreads), end='')

input('\n[*] Press enter to exit')
