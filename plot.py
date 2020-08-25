import matplotlib.pyplot as plot
import numpy as np

def wave_plot(x_values, amplitude):
    plot.plot(x_values, amplitude)

    plot.title('Wave')
    plot.xlabel('Time')
    plot.ylabel('Amplitude')

    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')

    plot.show()

