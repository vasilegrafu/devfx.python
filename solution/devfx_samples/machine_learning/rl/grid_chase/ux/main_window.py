import itertools as it
import time as t
import devfx.exceptions as exps
import devfx.core as core
import devfx.diagnostics as dgn
import devfx.machine_learning as ml
import devfx.parallel.threading as parallel
import devfx.ux.windows.wx as ux

from ..logic.grid_environment import GridEnvironment
from ..logic.grid_agent_kind import GridAgentKind

class MainWindow(ux.Window):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.__init_model()

        self.__init_widgets()
        self.__init_layout()

    """------------------------------------------------------------------------------------------------
    """
    def __init_model(self):
        self.training_grid_environment = GridEnvironment()
        self.training_grid_environment.create()
        self.viewable_grid_environment = GridEnvironment()
        self.viewable_grid_environment.create()
        
        for training_agent in self.training_grid_environment.get_agents():
            viewable_agent = self.viewable_grid_environment.get_agent(training_agent.get_id())
            training_agent.share_policy_with(viewable_agent)

    """------------------------------------------------------------------------------------------------
    """
    def __init_widgets(self):
        self.grid_canvas = ux.Canvas(self, size=(64, 64))
        self.grid_canvas.OnDraw += self.__grid_canvas__OnDraw

        self.agent_randomness_label = ux.Text(self, label='Randomness:') 
        self.agent_randomness_combobox = ux.ComboBox(self, choices=[str(agent.get_id()) + '|' + agent.get_name() for agent in self.viewable_grid_environment.get_agents()])
        self.agent_randomness_combobox.SetSelection(0)
        def agent_randomness_combobox__OnItemSelected(sender, event_args): 
            self.agent_randomness_spinbox.SetValue(self.viewable_grid_environment.get_agent(id=int(self.agent_randomness_combobox.GetValue().split('|')[0])).get_randomness())
            self.grid_canvas.UpdateDrawing()
        self.agent_randomness_combobox.OnItemSelected += agent_randomness_combobox__OnItemSelected
        self.agent_randomness_spinbox = ux.FloatSpinBox(self, min=0.0, max=1.0, initial=0.0, inc=0.01, size=(64, -1))
        self.agent_randomness_spinbox.SetValue(self.viewable_grid_environment.get_agent(id=int(self.agent_randomness_combobox.GetValue().split('|')[0])).get_randomness())
        def agent_randomness_spinbox_OnValueChanged(sender, event_args): 
            self.viewable_grid_environment.get_agent(id=int(self.agent_randomness_combobox.GetValue().split('|')[0])).set_randomness(self.agent_randomness_spinbox.GetValue())
            self.grid_canvas.UpdateDrawing()
        self.agent_randomness_spinbox.OnValueChanged += agent_randomness_spinbox_OnValueChanged

        self.train_button = ux.Button(parent=self, label='Train')
        self.train_button.OnPress += self.__train_button__OnPress
        self.cancel_training_button = ux.Button(parent=self, label='Cancel training')
        self.cancel_training_button.OnPress += self.__cancel_training_button__OnPress
        self.train_count_text = ux.Text(parent=self, label='0')
        self.training_is_running = False
        
        self.do_iteration_button = ux.Button(parent=self, label='Do iteration')
        self.do_iteration_button.OnPress += self.__do_iteration_button__OnPress
        
        self.do_iterations_speed_label = ux.Text(self, label='Speed:')
        self.do_iterations_speed_spinbox = ux.FloatSpinBox(self, min=0.01, max=1.0, initial=0.10, inc=0.01, size=(64, -1))
        self.do_iterations_button = ux.Button(parent=self, label='Do iterations')
        self.do_iterations_button.OnPress += self.__do_iterations_button__OnPress
        self.cancel_iterations_button = ux.Button(parent=self, label='Cancel iterations')
        self.cancel_iterations_button.OnPress += self.__cancel_iterations_button__OnPress
        self.do_iterations_is_running = False

    def __init_layout(self):
        #
        self.main_sizer = ux.GridBagSizer().AddToWindow(self)
        self.grid_sizer = ux.GridBagSizer().AddToSizer(self.main_sizer, pos=(0, 0), flag=ux.EXPAND)
        self.grid_sizer.AddGrowableCol(0)
        self.grid_sizer.AddGrowableRow(0)
        self.command_sizer = ux.GridBagSizer(hgap=32).AddToSizer(self.main_sizer, pos=(1, 0), flag=ux.ALIGN_CENTER)
        self.main_sizer.AddGrowableCol(0)
        self.main_sizer.AddGrowableRow(0, 1)
        self.main_sizer.AddGrowableRow(1, 0)

        self.training_sizer = ux.BoxSizer(ux.HORIZONTAL).AddToSizer(self.command_sizer, pos=(0, 0), span=(1, 2), flag=ux.ALIGN_RIGHT | ux.TOP, border=4)
        self.agent_settings_sizer = ux.BoxSizer(ux.HORIZONTAL).AddToSizer(self.command_sizer, pos=(1, 0), span=(2, 1), flag=ux.ALIGN_CENTER_VERTICAL | ux.ALIGN_RIGHT)
        self.do_iteration_sizer = ux.BoxSizer(ux.HORIZONTAL).AddToSizer(self.command_sizer, pos=(1, 1), flag=ux.ALIGN_RIGHT | ux.TOP, border=4)
        self.do_iterations_sizer = ux.BoxSizer(ux.HORIZONTAL).AddToSizer(self.command_sizer, pos=(2, 1), flag=ux.ALIGN_RIGHT | ux.TOP | ux.BOTTOM, border=4)

        # 
        self.grid_canvas.AddToSizer(self.grid_sizer, pos=(0, 0), flag=ux.ALIGN_CENTER | ux.SHAPED)

        self.agent_randomness_label.AddToSizer(self.agent_settings_sizer, flag=ux.ALIGN_CENTER_VERTICAL)
        self.agent_randomness_combobox.AddToSizer(self.agent_settings_sizer, flag=ux.ALIGN_CENTER_VERTICAL | ux.LEFT, border=2) 
        self.agent_randomness_spinbox.AddToSizer(self.agent_settings_sizer, flag=ux.ALIGN_CENTER_VERTICAL | ux.LEFT, border=2) 

        self.train_button.AddToSizer(self.training_sizer, flag=ux.ALIGN_CENTER_VERTICAL)
        self.cancel_training_button.AddToSizer(self.training_sizer, flag=ux.ALIGN_CENTER_VERTICAL | ux.LEFT, border=4) 
        self.train_count_text.AddToSizer(self.training_sizer, flag=ux.ALIGN_CENTER_VERTICAL | ux.LEFT, border=4) 

        self.do_iteration_button.AddToSizer(self.do_iteration_sizer, flag=ux.ALIGN_CENTER_VERTICAL)

        self.do_iterations_speed_label.AddToSizer(self.do_iterations_sizer, flag=ux.ALIGN_CENTER_VERTICAL)
        self.do_iterations_speed_spinbox.AddToSizer(self.do_iterations_sizer, flag=ux.ALIGN_CENTER_VERTICAL | ux.LEFT, border=2) 
        self.do_iterations_button.AddToSizer(self.do_iterations_sizer, flag=ux.ALIGN_CENTER_VERTICAL | ux.LEFT, border=4) 
        self.cancel_iterations_button.AddToSizer(self.do_iterations_sizer, flag=ux.ALIGN_CENTER_VERTICAL | ux.LEFT, border=4)

    """------------------------------------------------------------------------------------------------
    """
    def __grid_canvas__OnDraw(self, sender, event_args):
        cgc = event_args.CGC

        # cell size
        cell_width = cgc.GetSize()[0]/(self.viewable_grid_environment.shape[0] - 2)
        cell_height = cgc.GetSize()[1]/(self.viewable_grid_environment.shape[1] - 2)

        # draw grid
        for (cell_index, cell_content) in self.viewable_grid_environment.get_cells().items():
            x = (cell_index[1] - 2)*cell_width 
            y = (cell_index[0] - 2)*cell_height
            w = cell_width
            h = cell_height
            if(cell_content is None):
                cgc.DrawRectangle(x=x, y=y, w=w, h=h, pen=ux.BLACK_PEN, brush=ux.BLACK_BRUSH)
            else:
                cgc.DrawRectangle(x=x, y=y, w=w, h=h, pen=ux.BLACK_PEN, brush=ux.WHITE_BRUSH)

        # draw agents
        for agent in self.viewable_grid_environment.get_agents():
            cell_index = agent.get_state().value[0]
            x = (cell_index[1] - 2)*cell_width + cell_width/2
            y = (cell_index[0] - 2)*cell_height + cell_height/2
            agent_kind = agent.get_kind()
            if(agent_kind == GridAgentKind.CHASER):
                r = min(cell_width/4, cell_height/4)
                cgc.DrawCircle(x=x, y=y, r=r, pen=ux.BLACK_PEN, brush=ux.RED_BRUSH)
            elif(agent_kind == GridAgentKind.CHASED):
                r = min(cell_width/5, cell_height/5)
                cgc.DrawCircle(x=x, y=y, r=r, pen=ux.BLACK_PEN, brush=ux.LIME_BRUSH)
            else:
                raise exps.ApplicationError()
    
    """------------------------------------------------------------------------------------------------
    """
    def __train_button__OnPress(self, sender, event_args):
        if(self.training_is_running):
            return
        self.training_is_running = True

        def _():
            agents_iterator = core.ObjectStorage.intercept(self, 'training_agents_iterator', lambda: it.cycle(self.training_grid_environment.get_agents()))
            i = 0
            while self.training_is_running:
                agent = next(agents_iterator)
                self.training_grid_environment.do_iteration(agents=(agent,), randomness=1.0)
                i += 1
                if(i % 10000 == 0):
                    self.train_count_text.Label = str(i)
        thread = parallel.Thread().target(fn=_)
        thread.start()

    def __cancel_training_button__OnPress(self, sender, event_args):
        if(not self.training_is_running):
            return
        self.training_is_running = False

    """------------------------------------------------------------------------------------------------
    """
    def __do_iteration_button__OnPress(self, sender, event_args):
        agents_iterator = core.ObjectStorage.intercept(self, 'viewable_agents_iterator', lambda: it.cycle(self.viewable_grid_environment.get_agents()))
        agent = next(agents_iterator)
        self.viewable_grid_environment.do_iteration(agents=(agent,))
        self.grid_canvas.UpdateDrawing()  

    """------------------------------------------------------------------------------------------------
    """
    def __do_iterations_button__OnPress(self, sender, event_args):
        if(self.do_iterations_is_running):
            return
        self.do_iterations_is_running = True

        self.do_iteration_sizer.DisableChildren()

        def _():
            agents_iterator = core.ObjectStorage.intercept(self, 'viewable_agents_iterator', lambda: it.cycle(self.viewable_grid_environment.get_agents()))
            while self.do_iterations_is_running:
                agent = next(agents_iterator)
                self.viewable_grid_environment.do_iteration(agents=(agent,))
                self.grid_canvas.UpdateDrawing()
                t.sleep(self.do_iterations_speed_spinbox.GetValue())          
        thread = parallel.Thread().target(fn=_)
        thread.start()

    def __cancel_iterations_button__OnPress(self, sender, event_args):
        if(not self.do_iterations_is_running):
            return
        self.do_iterations_is_running = False

        self.do_iteration_sizer.EnableChildren()
