import devfx.statistics as stats
import devfx.data_vizualization as dv

"""------------------------------------------------------------------------------------------------
""" 
normal = stats.distributions.normal(mu=0.0, sigma=1.0)

figure = dv.Figure(size=(8, 4))

chart = dv.Chart2d(figure=figure)
stats.estimators.cdhistogram.from_distribution(normal).on_chart(chart).bar()

figure.show()

