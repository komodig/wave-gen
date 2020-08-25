import matplotlib.pyplot as plot

def single_plot(time, fx):
    plot.plot(time, fx, color='purple')

    plot.title('Wave')
    plot.xlabel('Time')
    plot.ylabel('Amplitude')

    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')

    plot.show()

def dual_plot(time, fx1, fx2):
    plot.plot(time, fx1, color='purple')
    plot.plot(time, fx2, color='blue')

    plot.title('Wave')
    plot.xlabel('Time')
    plot.ylabel('Amplitude')

    plot.grid(True, which='both')
    plot.axhline(y=0, color='k')

    plot.show()

