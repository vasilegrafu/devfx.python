import numpy as np
import devfx.exceptions as exps
import devfx.core as core

class Runner(object):
    def __init__(self, agents):
        self.__set_agents(agents=agents)

        self.running_status = core.EventHandler()

    """------------------------------------------------------------------------------------------------
    """ 
    def __set_agents(self, agents):
        self.__agents = agents
                
    def get_agents(self):
        return self.__agents

    """------------------------------------------------------------------------------------------------
    """
    @property
    def running_status(self):
        return self.__running_status

    @running_status.setter
    def running_status(self, event_handler):
        self.__running_status = event_handler

    """------------------------------------------------------------------------------------------------
    """
    class RunningCancellationToken(object):
        def __init__(self):
            self.__is_cancellation_requested = False

        def request_cancellation(self, condition=None):
            if (condition is None):
                self.__is_cancellation_requested = True
            elif (condition is not None):
                if(condition):
                    self.__is_cancellation_requested = True
            else:
                raise exps.NotSupportedError()

        def is_cancellation_requested(self):
            return (self.__is_cancellation_requested == True)

    """------------------------------------------------------------------------------------------------
    """
    class RunningParameters(object):
        def __init__(self, agents):
            self.agents = agents
            self.cancellation_token = Runner.RunningCancellationToken()

        @property
        def agents(self):
            return self.__agents

        @agents.setter
        def agents(self, value):
            self.__agents = value

        
        @property
        def continuing_agents(self):
            return self.__continuing_agents

        @continuing_agents.setter
        def continuing_agents(self, value):
            self.__continuing_agents = value

        
        @property
        def episodic_agents(self):
            return self.__episodic_agents

        @episodic_agents.setter
        def episodic_agents(self, value):
            self.__episodic_agents = value


        @property
        def cancellation_token(self):
            return self.__cancellation_token

        @cancellation_token.setter
        def cancellation_token(self, value):
            self.__cancellation_token = value

    """------------------------------------------------------------------------------------------------
    """
    def run(self, *args, **kwargs):
        self._run(*args, **kwargs)

    def _run(self, *args, **kwargs):
        raise exps.NotImplementedError()
        
