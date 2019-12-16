import numpy as np
import devfx.math as math
import devfx.machine_learning.tensorflow as ml
import devfx.neural_networks.tensorflow as nn
import devfx.data_vizualization.seaborn as dv

cg.enable_imperative_execution_mode()

"""------------------------------------------------------------------------------------------------
"""
def test():
    def f(L, k):
        x = cg.constant(math.range(-16.0, +16.0, 0.01), dtype=cg.float32)
        y = nn.activation.softsign(x, L, k)
        return x.numpy(), y.numpy()

    chart = dv.Chart2d(fig_size=(6, 4))
    chart.plot(*f(1.0, 1.0), color='blue')
    chart.plot(*f(2.0, 1.0), color='red')
    chart.plot(*f(1.0, 1.0/2.0), color='yellow')
    chart.figure.show()

if __name__ == '__main__':
    test()
