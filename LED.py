import math
import numpy as np
import matplotlib.pyplot as plt

class LED(object):
    """
    """
    def __init__(self,
                 I_0: float = 10000.,
                 m: float = 1.,
                 x_l: float = 0.,
                 y_l: float = 0.,
                 z_l: float = 10.,
                 gamma_1: float = 45.,
                 gamma_2: float = 0.):
        super(LED, self).__init__()
        self.I_0 = I_0
        self.m = m
        self.x_l = x_l
        self.y_l = y_l
        self.z_l = z_l
        self.gamma_1 = gamma_1
        self.gamma_2 = gamma_2
        pass

    def out(self):
        return {"I_0": self.I_0, "m": self.m, "x_l": self.x_l, "y_l": self.y_l, "z_l": self.z_l,
                "gamma_1": self.gamma_1, "gamma2": self.gamma_2}

    pass


class Surface(object):
    def __init__(self, center_x: float = 0., center_y: float = 0., center_z: float = 0., width: float = 100.,
                 length: float = 100., bins: tuple = (100, 100)):
        super(Surface, self).__init__()
        self.center_x = center_x
        self.center_y = center_y
        self.center_z = center_z
        self.width = width
        self.length = length
        self.bins = bins
        pass

    def surface(self, bins=None):
        if bins is None:
            bins = self.bins
            pass

        surface = np.zeros(shape=(2, bins[0], bins[1]))
        X = np.linspace(start=(self.center_x - self.length / 2), stop=(self.center_x + self.length / 2), num=bins[0])
        Y = np.linspace(start=(self.center_y - self.width / 2), stop=(self.center_y + self.width / 2), num=bins[1])
        for i in range(bins[1]):
            surface[0, :, i] = X
            pass
        for j in range(bins[0]):
            surface[1, j, :] = Y
            pass
        return surface

def cal(surface: np.ndarray = np.zeros((2,100, 100)), LEDs=None):
    if LEDs is None:
        LEDs = {'I_0': 10000.0, 'm': 0.0, 'x_l': 0.0, 'y_l': 0.0, 'z_l': 0.0, 'gamma_1': 0.0, 'gamma2': 0.0}
        pass
    [_,bins_0, bins_1] = surface.shape
    beta = np.zeros((bins_0, bins_1))
    # alpha = np.zeros((bins_0, bins_1))
    d = np.ones((bins_0,bins_1))

    for i in range(bins_0):
        for j in range(bins_1):
            beta[i,j] = math.sqrt((surface[0,i,j]-LEDs["x_l"])**2+(surface[1,i,j]-LEDs["y_l"])**2)/LEDs["z_l"]
            d[i,j] = math.sqrt(((surface[0,i,j]-LEDs["x_l"])**2+(surface[1,i,j]-LEDs["y_l"])**2)+LEDs["z_l"]**2)
            pass
        pass
    beta = np.arctan(beta)
    beta_d = np.degrees(beta)
    alpha_d = abs(90- LEDs["gamma_1"]-beta_d)
    alpha = alpha_d/180*math.pi


    out_surface = np.zeros((bins_0,bins_1))
    for i in range(bins_0):
        for j in range(bins_1):
            out_surface[i,j] = LEDs["I_0"]*math.cos(alpha[i,j])**LEDs["m"]*math.cos(beta[i,j])*d[i,j]**(-2)
            pass
        pass
    return out_surface


# Led_1 = LED().out()
# Sur = Surface().surface()
#
# data = cal(surface=Sur,LEDs=Led_1)
# print(Led_1)
# plt.imshow(data)
# plt.colorbar()
# plt.show()

Led_1 = LED(z_l=80,x_l=40,gamma_1=90).out()
Led_2 = LED(z_l=80,x_l=-20,gamma_1=90).out()

Sur = Surface(center_x=0,width=200,length=200).surface(bins=(100,100))



data = cal(surface=Sur, LEDs=Led_1)
data_1 = cal(surface=Sur,LEDs=Led_2)


plt.imshow(data_1+data)
plt.colorbar()
plt.show()









#
#
#     def illu(self, alpha: float = None, beta: float = None, d: float = None):
#         if alpha is None:
#             alpha = 0.  # unit: degree
#             pass
#         if beta is None:
#             beta = 0.  # unit: degree
#             pass
#         if d is None:
#             d = 100.  # unit: mm
#             pass
#         E = self.I_0 * (math.cos(alpha) ** self.m) * math.cos(beta) * d ** (-2)
#         return E
#
# # 等会再创建一个面的类
