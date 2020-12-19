import random as rnd
import numpy as np
import devfx.exceptions as excs
from .policy import Policy

class ESarsaPolicy(Policy):
    def __init__(self, discount_factor, learning_rate):
        super().__init__(discount_factor=discount_factor)

        self.__table = {}
        self.__learning_rate = learning_rate

    """------------------------------------------------------------------------------------------------
    """ 
    def get_states(self):
        return self.__table.keys()

    def get_actions(self, state):
        return self.__table[state].keys()

    def set_value(self, state, action, value):
        if(state not in self.__table):
            self.__table[state] = {}
        self.__table[state][action] = value

    def get_value(self, state, action):
        return self.__table[state][action]

    def has_value(self, state, action):
        if(state not in self.__table):
            return False
        if(action not in self.__table[state]):
            return False
        return True

    """------------------------------------------------------------------------------------------------
    """ 
    def get_learning_rate(self):
        return self.__learning_rate

    def set_learning_rate(self, learning_rate):
        self.__learning_rate = learning_rate

    """------------------------------------------------------------------------------------------------
    """
    def _learn(self, state, action, next_state_and_reward):
        if(state not in self.__table):
            self.__table[state] = {}
        if(action not in self.__table[state]):
            self.__table[state][action] = 0.0

        (next_state, next_reward) = next_state_and_reward
        if(next_state not in self.__table):
            error = next_reward.value - self.__table[state][action]
        else:
            error = next_reward.value + self.get_discount_factor()*sum(self.__table[next_state].values())/len(self.__table[next_state]) - self.__table[state][action]
        self.__table[state][action] = self.__table[state][action] + self.get_learning_rate()*error

    """------------------------------------------------------------------------------------------------
    """
    def _get_optimal_action(self, state):
        if(state not in self.__table):
             return None
        if(len(self.__table[state]) == 0):
            return None
                      
        action = max(self.__table[state], key=lambda action: self.__table[state][action])
        return action

    """------------------------------------------------------------------------------------------------
    """ 
    def _copy(self):
        policy = ESarsaPolicy(discount_factor=self.get_discount_factor(), learning_rate=self.get_learning_rate())
        for state in self.get_states():
            for action in self.get_actions(state):
                policy.set_value(state=state, action=action, value=self.get_value(state, action))
        return policy

    """------------------------------------------------------------------------------------------------
    """ 
    def _assign_from(self, policies):
        raise excs.NotImplementedError()




    