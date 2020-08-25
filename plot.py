import matplotlib.pyplot as plot

def wave_plot(time, fx):
    plot.plot(time, fx)

    plot.title('Wave')
    plot.xlabel('Time')
    plot.ylabel('Amplitude')

    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')

    plot.show()

