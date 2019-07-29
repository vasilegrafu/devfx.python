import numpy as np
import devfx.statistics as stats
import devfx.computation_graphs.tensorflow as cg
import devfx.data_vizualization.seaborn as dv

"""------------------------------------------------------------------------------------------------
"""
class QuadraticRegressionDataGenerator(object):
    def __init__(self):
        pass

    def generate(self):
        M = 1024*4
        a = -1.0
        b = 8.0
        c = 0
        x = np.random.normal(0.0, 4.0, size=M)
        y = a*x*x + b*x + c + np.random.normal(0.0, 8.0, size=M)
        return [x, y]

"""------------------------------------------------------------------------------------------------
"""
class QuadraticRegressionModel(cg.models.DeclarativeModel):
    # ----------------------------------------------------------------
    def _build_model(self):
        # hypothesis
        x = cg.placeholder(shape=[None], name='x')
        w0 = cg.create_variable(name='w0', shape=[1], initializer=cg.zeros_initializer())
        w1 = cg.create_variable(name='w1', shape=[1], initializer=cg.zeros_initializer())
        w2 = cg.create_variable(name='w2', shape=[1], initializer=cg.zeros_initializer())
        h = w0 + w1*x + w2*x*x

        # cost function
        y = cg.placeholder(shape=[None], name='y')
        J = 0.5*cg.reduce_mean(cg.square(h-y))

        # evaluators
        self.register_input_evaluator(input=input)
        self.register_evaluator(name='weight', evaluatee=[w0, w1, w2])
        self.register_output_evaluator(output=y)
        self.register_hypothesis_evaluator(hypothesis=h, input=x)
        self.register_cost_evaluator(cost=J, input=x, output=y)

        # cost minimizer
        self.register_cost_optimizer_applier_evaluator(cost=J, input=x, output=y, optimizer=cg.train.AdamOptimizer(learning_rate=1e-2))

    # ----------------------------------------------------------------
    def _on_training_begin(self, context):
        context.append_to_training_log_condition = lambda context: context.iteration % 100 == 0

    def _on_training_epoch_begin(self, epoch, context):
        pass

    def _on_append_to_training_log(self, training_log, context):
        training_log.last_item.training_data_cost = self.run_cost_evaluator(*context.training_data)
        if(len(training_log.nr_list) >= 2):
            training_log.last_item.trend_of_training_data_cost = stats.regression.normalized_trend(x=training_log.nr_list, y=training_log.training_data_cost_list, n_max=32)[0][1]
            context.cancellation_token.request_cancellation(condition=(abs(training_log.last_item.trend_of_training_data_cost) <= 1e-2))

        training_log.last_item.test_data_cost = self.run_cost_evaluator(*context.test_data)

        print(training_log.last_item)

        figure, chart = dv.PersistentFigure(id='status', size=(8, 6), chart_fns=[lambda _: dv.Chart2d(figure=_)])
        chart.plot(training_log.training_data_cost_list, color='green')
        chart.plot(training_log.test_data_cost_list, color='red')
        figure.refresh()

    def _on_training_epoch_end(self, epoch, context):
        pass

    def _on_training_end(self, context):
        pass

"""------------------------------------------------------------------------------------------------
"""
def main():
    # generating data
    generated_data = QuadraticRegressionDataGenerator().generate()

    figure = dv.Figure(size=(8, 6))
    chart = dv.Chart2d(figure=figure)
    chart.scatter(generated_data[0], generated_data[1])
    figure.show()

    # preprocessing data
    # generated_data[0] = (generated_data[0] - stats.series.center.mean(generated_data[0]))/stats.series.dispersion.stddev(generated_data[0])

    # splitting data
    split_bound = int(0.75*len(generated_data[0]))
    training_data = [_[:split_bound] for _ in generated_data] 
    test_data = [_[split_bound:] for _ in generated_data] 
    # print(training_data, test_data)

    # learning from data
    model = QuadraticRegressionModel()
    model.train(training_data=training_data, batch_size=256,
                test_data=test_data)

    # model validation
    figure = dv.Figure(size=(8, 6))
    chart = dv.Chart2d(figure=figure)
    chart.scatter(test_data[0], test_data[1], color='blue')
    chart.scatter(test_data[0], model.run_hypothesis_evaluator(input_data=test_data[0]), color='red')
    figure.show()

    model.close()
    
"""------------------------------------------------------------------------------------------------
"""
if __name__ == '__main__':
    main()

