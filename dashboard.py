import time
import threading
from tkinter import *
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import mpl_toolkits.mplot3d.axes3d as p3

from communication.client.client import MountainClient


class Dashboard:
    def __init__(self, client: MountainClient):
        self.root = Tk()
        self.root.title("Dashboard")
        
        self.client = client
        self.data = client.get_data()

        self.time_step = 500 # ms
        self.animations = [] # for animations to stay alive in memory
        self.figsize = (4.5, 3)
        self.mountain_radius = 23000
        self.frames = []
        
        self.frames.append(LabelFrame(self.root, text="Heights of hikers through time", padx=5, pady=5))
        self.frames[0].grid(row=0, column=0, padx=10, pady=10)
        self.plot_heights(self.frames[0])
        
        self.frames.append(LabelFrame(self.root, text="Skyview of hikers trajectories", padx=5, pady=5))
        self.frames[1].grid(row=0, column=1, padx=10, pady=10)
        self.plot_xy(self.frames[1])
        
        self.frames.append(LabelFrame(self.root, text="Mountain", padx=5, pady=5))
        self.frames[2].grid(row=1, column=0, padx=10, pady=10)
        self.plot_mountain(self.frames[2], grid_size=20) 

        self.frames.append(LabelFrame(self.root, text="Radar", padx=5, pady=5))
        self.frames[3].grid(row=1, column=1, padx=10, pady=10)
        self.plot_radar(self.frames[3])      

    def plot_heights(self, frame):
        fig, ax = plt.subplots(figsize=self.figsize)
        plt.subplots_adjust(left=0.15, right=0.75)
        ax.set_xlim(0, 5000)
        ax.set_ylim(0, 5100)
        team = list(self.data.keys())[0]
        lines = {hiker: ax.plot(0,0, label=hiker)[0] for hiker in self.data[team]}
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        x_data = []
        y_data = {hiker: [] for hiker in self.data[team]}

        def animate(i):
            x_data.append(i)

            for hiker in self.data[team]:
                hiker_data = self.data[team][hiker]
                y_data[hiker].append(hiker_data['z'])
                lines[hiker].set_ydata(y_data[hiker])
                lines[hiker].set_xdata(x_data)
            return lines.values()

        self.animations.append(FuncAnimation(fig, func=animate, interval=self.time_step, blit=True))

        canvas = FigureCanvasTkAgg(fig, frame)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack()

    def plot_xy(self, frame):
        fig, ax = plt.subplots(figsize=self.figsize)
        plt.subplots_adjust(left=0.2, right=0.75)
        ax.set_xlim(-self.mountain_radius, self.mountain_radius)
        ax.set_ylim(-self.mountain_radius, self.mountain_radius)
        team = list(self.data.keys())[0]
        lines = {hiker: ax.plot(0,0, label=hiker)[0] for hiker in self.data[team]}
        circle = plt.Circle((0, 0), self.mountain_radius, color='k', ls='--', fill=False)
        ax.add_patch(circle)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        
        x_data = {hiker: [] for hiker in self.data[team]}
        y_data = {hiker: [] for hiker in self.data[team]}

        def animate(i):
            for hiker in self.data[team]:
                hiker_data = self.data[team][hiker]
                x_data[hiker].append(hiker_data['x'])
                y_data[hiker].append(hiker_data['y'])
                lines[hiker].set_ydata(y_data[hiker])
                lines[hiker].set_xdata(x_data[hiker])
            return lines.values()

        self.animations.append(FuncAnimation(fig, func=animate, interval=self.time_step, blit=True))

        canvas = FigureCanvasTkAgg(fig, frame)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack()

    def plot_mountain(self, frame, grid_size=10):

        fig = plt.figure(figsize=self.figsize)
        plt.subplots_adjust(left=0.15, right=0.75)
        ax = p3.Axes3D(fig, auto_add_to_figure=False)
        fig.add_axes(ax)
        my_cmap = plt.get_cmap("terrain")
        min_height = 0
        max_height = 5500
        rescale = lambda y: (y - (min_height)) / ((max_height) - (min_height))
        heights = {}
        bar_width = (self.mountain_radius*2) // grid_size
        bar_height = (self.mountain_radius*2) // grid_size
        for i in range(-self.mountain_radius, self.mountain_radius+1, bar_width):
            for j in range(-self.mountain_radius, self.mountain_radius+1, bar_height):
                heights[(i, j)] = {'sum': 0, 'count': 0}

        # add bars
        bars = {}
        for i in range(-self.mountain_radius, self.mountain_radius+1, bar_width):
            for j in range(-self.mountain_radius, self.mountain_radius+1, bar_height):
                bars[(i,j)] = ax.bar3d(i, j, 0, bar_width, bar_height, 0, color=my_cmap(0))

        def update_bars(num, bars):
            for team in self.data:
                for hiker in self.data[team]:
                    
                    # get position in grid
                    i = (self.data[team][hiker]['x'] + self.mountain_radius) // bar_width * bar_width - self.mountain_radius
                    j = (self.data[team][hiker]['y'] + self.mountain_radius) // bar_height * bar_height - self.mountain_radius

                    heights[(i,j)]['sum'] += self.data[team][hiker]['z']
                    heights[(i,j)]['count'] += 1
                    avg_height = heights[(i,j)]['sum']/heights[(i,j)]['count']
                    bars[(i,j)] = ax.bar3d(i, j, 0, bar_width, bar_height, avg_height, color=my_cmap(rescale(avg_height)))
            return bars.values()
        
        self.animations.append(FuncAnimation(fig, update_bars, 20, fargs=[bars], interval=self.time_step, blit=False))

        canvas = FigureCanvasTkAgg(fig, frame)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack()

    def plot_radar(self, frame):
        fig, ax = plt.subplots(figsize=self.figsize)
        plt.subplots_adjust(left=0.2, right=0.75)
        ax.set_xlim(-self.mountain_radius, self.mountain_radius)
        ax.set_ylim(-self.mountain_radius, self.mountain_radius)
        team = list(self.data.keys())[0]
        xs = []
        ys = []
        for hiker in self.data[team]:
            x = self.data[team][hiker]['x']
            y = self.data[team][hiker]['y']
            xs.append(x)
            ys.append(y)
        scats = {team: ax.scatter(xs, ys, s=5, label=team)}
        circle = plt.Circle((0, 0), self.mountain_radius, color='k', ls='--', fill=False)
        ax.add_patch(circle)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        def update(i):
            xs = []
            ys = []
            labels = []
            for hiker in self.data[team]:
                x = self.data[team][hiker]['x']
                y = self.data[team][hiker]['y']
                xs.append(x)
                ys.append(y)
                labels.append(hiker)
            scats[team].set_offsets(list(zip(xs,ys)))
            return scats.values()

        self.animations.append(FuncAnimation(fig, update, interval=self.time_step, blit=True))

        canvas = FigureCanvasTkAgg(fig, frame)
        toolbar = NavigationToolbar2Tk(canvas, frame)
        toolbar.update()
        canvas._tkcanvas.pack()

    def start(self):
        t = threading.Thread(target=self.update_data)
        t.start()
        self.root.mainloop()  

    def update_data(self):
        while not self.client.is_over():
            self.data = self.client.get_data()
            time.sleep(self.time_step/1000)

    def stop(self):
        self.root.quit()

if __name__ == "__main__":
    # client = MountainClient('10.42.0.1', 8888)
    client = MountainClient('172.16.0.219', 8888)
    # client = MountainClient('localhost', 8080)
    d = Dashboard(client)
    d.start()