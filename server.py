import time
import threading

from communication.client.client import MountainClient
from communication.server.server import MountainServer
from communication.server.mountain.easy_mountain import EasyMountain
from communication.server.mountain.mccormick_mountain import McCormickMountain
from communication.server.mountain.mishra_mountain import MishraBirdMountain
from communication.server.mountain.rastrigin_mountain import RastriginMountain
from communication.server.mountain.ackley_mountain import AckleyMountain
from communication.server.mountain.easom_mountain import EasomMountain
from communication.server.mountain.sinosidal_mountain import SinosidalMountain
from communication.server.mountain.abstract.mountain import Mountain
from communication.util.logger import logger

def main():
    i = 0
    while True:
        print('Ctrl + C now or server will restart in 5 seconds')
        time.sleep(5)

        ip = '0.0.0.0'
        port = 8888
        thread = threading.Thread(target = finish_registration, args=(ip, port))
        visual_radius = 50
        base_radius = 23000
        mountains = [EasyMountain, McCormickMountain, MishraBirdMountain, RastriginMountain, AckleyMountain, EasomMountain, SinosidalMountain]

        mountain = mountains[i % len(mountains)](visual_radius, base_radius)
        logger.info(f"Current mountain: {str(mountain).split(' ')[0].split('.')[-1]}")
        server = MountainServer(mountain, (14000,14000), 50, ip, port)
        thread.start()
        server.start()
        i += 1

def finish_registration(ip, port):
    time.sleep(1)
    client = MountainClient(ip, port)
    logger.info('In 30 seconds, registration will be finished')
    time.sleep(30)
    client.finish_registration2()

if __name__ == '__main__':
    main()
