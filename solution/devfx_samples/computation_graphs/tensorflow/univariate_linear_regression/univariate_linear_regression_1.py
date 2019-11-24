import devfx.os as os
import numpy as np
import devfx.data_containers as dc
import devfx.statistics as stats
import devfx.computation_graphs.tensorflow as cg
import devfx.data_vizualization.seaborn as dv
import devfx.statistics.mseries as mseries

"""------------------------------------------------------------------------------------------------
"""
class UnivariateLinearRegressionDataGenerator():
    def __init__(self):
        pass

    def generate(self):
        M = 1024
        a = 1.0
        b = 0.75
        x = np.random.normal(0.0, 0.5, size=M)
        y = a*x + b + np.random.normal(0.0, 0.1, size=M)
        return [x, y]


"""------------------------------------------------------------------------------------------------
"""
class UnivariateLinearRegressionModel(cg.models.DeclarativeModel):
    # ----------------------------------------------------------------
    def _build_model(self):
        # hypothesis
        x = cg.placeholder(shape=[None], name='x')
        w0 = cg.create_variable(name='w0', shape=[1], initializer=cg.zeros_initializer())
        w1 = cg.create_variable(name='w1', shape=[1], initializer=cg.zeros_initializer())
        h = w0 + w1*x
        h = cg.identity(h, 'h')

        # cost function
        y = cg.placeholder(shape=[None], name='y')
        J = 0.5*cg.reduce_mean(cg.square(h-y))

        # evaluators
        self.register_input_evaluator(input=input)
        self.register_evaluator(name='weight', evaluatee=[w0, w1])
        self.register_output_evaluator(output=y)
        self.register_hypothesis_evaluator(hypothesis=h, input=x)
        self.register_cost_evaluator(cost=J, input=x, output=y)

        # cost minimizer 
        self.register_cost_optimizer_applier_evaluator(cost=J, input=x, output=y, optimizer=cg.train.AdamOptimizer(learning_rate=1e-2))

    # ----------------------------------------------------------------
    def _on_training_begin(self, context):
        context.append_to_training_log_condition = lambda context: context.iteration % 1 == 0

    def _on_training_epoch_begin(self, epoch, context):
        pass

    def _on_append_to_training_log(self, training_log, context):
        training_log.last_item.training_data_cost = self.run_cost_evaluator(*context.training_data)
        if(len(training_log.nr_list) >= 2):
            training_log.last_item.trend_of_training_data_cost = stats.regression.normalized_trend(x=training_log.nr_list, y=training_log.training_data_cost_list, n_max=32)[0][1]
            context.cancellation_token.request_cancellation(condition=(abs(training_log.last_item.trend_of_training_data_cost) <= 1e-2))

        training_log.last_item.test_data_cost = self.run_cost_evaluator(*context.test_data)
        
        training_log.last_item.w = [_[0] for _ in self.run_evaluator(name='weight')]

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
    generated_data = UnivariateLinearRegressionDataGenerator().generate()
    
    # shuffle
    generated_data = mseries.shuffle(generated_data)

    # chart
    figure = dv.Figure(size=(8, 6))
    chart = dv.Chart2d(figure=figure)
    chart.scatter(generated_data[0], generated_data[1])
    figure.show()

    # splitting data
    (training_data, test_data) = mseries.split(generated_data, int(0.75*mseries.rows_count(generated_data)))
    # print(training_data, test_data)

    # learning from data
    with UnivariateLinearRegressionModel() as model:
        model.train(training_data=training_data, batch_size=256,
                    test_data=test_data)
        model.export_to(os.file_info.parent_directorypath(__file__) + '/exports/_1')

    # validation
    with cg.models.ModelExecuter(os.file_info.parent_directorypath(__file__) + '/exports/_1') as model_executer:
        figure = dv.Figure(size=(8, 6))
        chart = dv.Chart2d(figure=figure)
        chart.scatter(test_data[0], test_data[1], color='blue')
        chart.scatter(test_data[0], model_executer.evaluate(fetch_names='h', feed_dict={'x': test_data[0]}), color='red')
        figure.show()

"""------------------------------------------------------------------------------------------------
"""
if __name__ == '__main__':
    main()
