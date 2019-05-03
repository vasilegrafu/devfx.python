import tensorflow as tf
import devfx.exceptions as exps

"""------------------------------------------------------------------------------------------------
"""
def enable_declarative_execution_mode():
    raise exps.NotSupportedError()

def enable_imperative_execution_mode():
    tf.enable_eager_execution()

"""------------------------------------------------------------------------------------------------
"""
def is_declarative_execution_mode_enabled():
    return not tf.executing_eagerly()

def is_imperative_execution_mode_enabled():
    return tf.executing_eagerly()