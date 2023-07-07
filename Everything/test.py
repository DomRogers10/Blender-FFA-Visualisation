import matplotlib
import matplotlib.pyplot
import math

def get_phi(r, phi0_degrees):
    phi = math.radians(phi0_degrees)-math.tan(math.radians(45))*math.log(r/1)
    return phi

r_list = [r for r in range(1, 21)]
phi_list_1 = [get_phi(r, 10.0) for r in r_list]
phi_list_2 = [get_phi(r, 20.0) for r in r_list]

figure = matplotlib.pyplot.figure()
axes = figure.add_subplot(1, 1, 1)
axes.plot(r_list, phi_list_1)
axes.plot(r_list, phi_list_2)
matplotlib.pyplot.show()



