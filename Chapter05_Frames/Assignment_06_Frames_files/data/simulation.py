from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np

class Simulation():
    def __init__(self, in_file, out_file):
        self.resolution = 75
        self.ship_pos = self.import_txt(in_file)
        self.final_pos = self.import_txt(out_file)
        
        self.fig = plt.figure()
        self.ax = plt.axes(projection='3d')
        plt.ion()
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        self.fig.show()
        self.fig.canvas.draw()

    def get_RZ(self, theta: float) -> np.array:
        R = np.array([[np.cos(theta), -np.sin(theta), 0.], 
                    [np.sin(theta), np.cos(theta),  0.], 
                    [0.,            0.,             1.]])
        return R

    def get_RX(self, theta: float) -> np.array:
        R = np.array([[1., 0.,             0.], 
                    [0., np.cos(theta), -np.sin(theta)], 
                    [0., np.sin(theta), np.cos(theta)]])
        return R

    def get_RY(self, theta: float) -> np.array:
        R = np.array([[np.cos(theta),  0., np.sin(theta)], 
                    [0.,             1., 0.], 
                    [-np.sin(theta), 0., np.cos(theta)]])
        return R

    def import_txt(self, file):
        file1 = open(file,"r")
        x = file1.readline()[:-1]
        y = file1.readline()[:-1]
        z = file1.readline()[:-1]
        x = np.array(x.split(", "), dtype = np.float64)
        y = np.array(y.split(", "), dtype = np.float64)
        z = np.array(z.split(", "), dtype = np.float64)
        file1.close()
        ship = np.vstack((x, y, z))
        return ship
    
    def check_success(self, new_pos):
        if np.all(np.equal(new_pos, self.final_pos)):
            return "MISSION SUCCESSFUL!!! You are on the right trajectory."
        else:
            return "SYSTEMS ERROR!!! You are off course."

    def animate(self, new_pos):
        self.ax.clear() 
        self.ax.set_xlim([-5, 5])
        self.ax.set_ylim([-5, 5])
        self.ax.set_zlim([-5, 5])
        self.ax.scatter(6, 0, 0, color='r', label='Alpha Centauri A', marker='*')
        self.ax.scatter(0, 6, 0, color='b', label='Sirius', marker='*')
        self.ax.scatter(0, 0, 6, color='g', label='Denebola', marker='*')
        verts = [list(zip(new_pos[0],new_pos[1],new_pos[2]))]
        self.ax.add_collection3d(Poly3DCollection(verts))
        self.ax.legend()
        self.fig.canvas.draw()

    def ang_seg(self, angle):
        return np.linspace(0, angle, self.resolution)

    def euler_continuous(self, alpha, beta, gamma):
        a = self.ang_seg(alpha)
        b = self.ang_seg(beta)
        g = self.ang_seg(gamma)
    
        for i in range(self.resolution):
            new_pos = self.get_RX(np.deg2rad(g[i])).dot(self.ship_pos)
            new_pos = self.get_RY(np.deg2rad(b[i])).dot(new_pos)
            new_pos = self.get_RZ(np.deg2rad(a[i])).dot(new_pos)
            self.animate(new_pos)

        
        plt.show()
        return self.check_success(np.round(new_pos, 2))

