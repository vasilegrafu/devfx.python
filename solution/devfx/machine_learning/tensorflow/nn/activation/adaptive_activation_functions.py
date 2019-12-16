import numpy as np
from ... import variables

from .activation_functions import identity

from .activation_functions import binary
from .activation_functions import sigmoid
from .activation_functions import bipolar
from .activation_functions import tanh
from .activation_functions import softsign

from .activation_functions import softmax

from .activation_functions import symlog
from .activation_functions import sympow

from .activation_functions import softplus
from .activation_functions import relu
from .activation_functions import loglu
from .activation_functions import powlu

"""------------------------------------------------------------------------------------------------
"""
def adaptive_identity(x, dx=0.0, dy=0.0, adaptive_dx=False, adaptive_dy=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    dy = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dy)) if(adaptive_dy) else dy
    return identity(x - dx) + dy

"""------------------------------------------------------------------------------------------------
"""
def adaptive_binary(x, dx=0.0, adaptive_dx=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    return binary(x - dx)

def adaptive_sigmoid(x, L=1.0, s0=1.0/4.0, dx=0.0, adaptive_L=False, adaptive_s0=False, adaptive_dx=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    L = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, L)) if(adaptive_L) else L
    s0 = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, s0)) if(adaptive_s0) else s0
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    return sigmoid(x - dx, L=L, s0=s0)

def adaptive_bipolar(x, dx=0.0, adaptive_dx=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    return bipolar(x - dx)

def adaptive_tanh(x, L=1.0, s0=1.0/4.0, dx=0.0, adaptive_L=False, adaptive_s0=False, adaptive_dx=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    L = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, L)) if(adaptive_L) else L
    s0 = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, s0)) if(adaptive_s0) else s0
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    return tanh(x - dx, L=L, s0=s0)

def adaptive_softsign(x, L=1.0, s0=1.0/4.0, dx=0.0, adaptive_L=False, adaptive_s0=False, adaptive_dx=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    L = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, L)) if(adaptive_L) else L
    s0 = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, s0)) if(adaptive_s0) else s0
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    return softsign(x - dx, L=L, s0=s0)

# ----------------------------------------------------------------
def adaptive_softmax(x, axis=-1, dx=0.0, adaptive_dx=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    return softmax(x - dx, axis=axis)

# ----------------------------------------------------------------
def adaptive_symlog(x, s0=1.0, b=np.e, dx=0.0, adaptive_s0=False, adaptive_b=False, adaptive_dx=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    s0 = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, s0)) if(adaptive_s0) else s0
    b = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, b)) if(adaptive_b) else b
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    return symlog(x - dx, s0=s0, b=b)

def adaptive_sympow(x, s0=1.0, n=2.0, dx=0.0, adaptive_s0=False, adaptive_n=False, adaptive_dx=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    s0 = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, s0)) if(adaptive_s0) else s0
    n = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, n)) if(adaptive_n) else n
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    return sympow(x - dx, s0=s0, n=n)

# ----------------------------------------------------------------
def adaptive_softplus(x, dx=0.0, dy=0.0, adaptive_dx=False, adaptive_dy=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    dy = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dy)) if(adaptive_dy) else dy
    return softplus(x - dx) + dy

def adaptive_relu(x, s0=1.0, a=1e-2, dx=0.0, dy=0.0, adaptive_s0=False, adaptive_a=False, adaptive_dx=False, adaptive_dy=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    s0 = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, s0)) if(adaptive_s0) else s0
    a = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, a)) if(adaptive_a) else a
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    dy = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dy)) if(adaptive_dy) else dy
    return relu(x - dx, s0=s0, a=a) + dy

def adaptive_loglu(x, s0=1.0, b=np.e, dx=0.0, dy=0.0, adaptive_s0=False, adaptive_b=False, adaptive_dx=False, adaptive_dy=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    s0 = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, s0)) if(adaptive_s0) else s0
    b = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, b)) if(adaptive_b) else b
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    dy = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dy)) if(adaptive_dy) else dy
    return loglu(x - dx, s0=s0, b=b) + dy

def adaptive_powlu(x, s0=1.0, n=2.0, dx=0.0, dy=0.0, adaptive_s0=False, adaptive_n=False, adaptive_dx=False, adaptive_dy=False):
    x_shape = tuple([_.value for _ in x.shape])
    x_M = x_shape[0]
    x_item_shape = x_shape[1:]
    s0 = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, s0)) if(adaptive_s0) else s0
    n = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, n)) if(adaptive_n) else n
    dx = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dx)) if(adaptive_dx) else dx
    dy = ml.Variable(dtype=x.dtype, initial_value=ml.fill(x_item_shape, dy)) if(adaptive_dy) else dy
    return powlu(x - dx, s0=s0, n=n) + dy