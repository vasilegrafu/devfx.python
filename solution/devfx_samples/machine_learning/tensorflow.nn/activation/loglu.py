import numpy as np
import devfx.math as math
import devfx.machine_learning.tensorflow as ml
import devfx.neural_networks.tensorflow as nn
import devfx.data_vizualization.seaborn as dv

cg.enable_imperative_execution_mode()

"""------------------------------------------------------------------------------------------------
"""
def test():
    def f(s0, b):
        x = cg.constant(math.range(-32.0, +16.0, 0.01), dtype=cg.float32)
        y = nn.activation.loglu(x, s0, b)
        return x.numpy(), y.numpy()

    chart = dv.Chart2d(fig_size=(6, 6))
    chart.plot(*f(1.0, np.e), color='yellow')
    chart.plot(*f(2.0, 3.0), color='blue')
    chart.plot(*f(1.0/2.0, 8.0*np.e), color='red')
    chart.figure.show()

if __name__ == '__main__':
    test()


