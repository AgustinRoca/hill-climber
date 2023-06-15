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

        ip = 'localhost'
        port = 8080
        thread = threading.Thread(target = finish_registration, args=(ip, port))
        visual_radius = 50
        base_radius = 23000
        mountains = [EasyMountain, McCormickMountain, MishraBirdMountain, RastriginMountain, AckleyMountain, EasomMountain, SinosidalMountain]

        mountain = mountains[i % len(mountains)](visual_radius, base_radius)
        logger.info(f"Current mountain: {str(mountain).split(' ')[0].split('.')[-1]}")
        server = MountainServer(mountain, (14000,14000), 50, 'localhost', 8080)
        # graph_mountain(mountain)
        thread.start()
        server.start()
        i += 1

def finish_registration(ip, port):
    client = MountainClient(ip, port)
    logger.info('In 30 seconds, registration will be finished')
    time.sleep(30)
    client.finish_registration()

def graph_mountain(mountain: Mountain):
    from matplotlib import cbook
    from matplotlib import cm
    from matplotlib.colors import LightSource
    import matplotlib.pyplot as plt
    import numpy as np

    # Load and format data
    
    nrows, ncols = (100, 100)
    xs = np.linspace(-23000, 23000, ncols)
    ys = np.linspace(-23000, 23000, nrows)
    zs = np.zeros((nrows, ncols))
    for i,y in enumerate(ys):
        for j,x in enumerate(xs):
            if not mountain.is_out_of_bounds(x, y):
                zs[i,j] = mountain.get_height(x, y)
    xs, ys = np.meshgrid(xs, ys)

    # Set up plot
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    ls = LightSource(270, 45)
    # To use a custom hillshading mode, override the built-in shading and pass
    # in the rgb colors of the shaded surface calculated from "shade".
    rgb = ls.shade(zs, cmap=cm.gist_earth, vert_exag=0.1, blend_mode='soft')
    surf = ax.plot_surface(xs, ys, zs, rstride=1, cstride=1, facecolors=rgb,
                        linewidth=0, antialiased=False, shade=False)

    offset = 0
    ax.scatter([14000], [14000], [mountain.get_height(14000, 14000) + offset])
    ax.scatter([mountain.flag[0]], [mountain.flag[1]], [mountain.get_height(mountain.flag[0], mountain.flag[1]) + offset])

    # surf = ax.plot_surface(xs, ys, zs, edgecolor='royalblue', lw=0.5, rstride=8, cstride=8, alpha=0.3)

    plt.show()

if __name__ == '__main__':
    main()