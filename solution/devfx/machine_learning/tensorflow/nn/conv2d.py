import tensorflow as tf
from .. import types
from .. import initializers
from .. import variables

def conv2d(name,
           input,
           filters_n,
           kernel_size,
           strides=(1, 1, 1, 1),
           padding='VALID',
           data_format='NHWC',  
           dtype=types.float32,
           kernel_initializer=None,
           bias_initializer=None,
           activation_fn=None):

    if(kernel_initializer is None):
        kernel_initializer = initializers.random_glorot_normal_initializer()

    if(bias_initializer is None):
        bias_initializer = initializers.random_glorot_normal_initializer()

    if (activation_fn is None):
        activation_fn = lambda x : x
    
    input_shape = tuple(input.shape)

    w_height = kernel_size[0]
    w_width = kernel_size[1]
    in_channels = input_shape[3]
    out_channels = filters_n
    w_shape = (w_height, w_width, in_channels, out_channels)
    w = variables.create_or_get_variable(name=f'{name}__w', shape=w_shape, dtype=dtype, initializer=kernel_initializer)
    
    conv = tf.nn.conv2d(input=input,  # [batch, in_height, in_width, in_channels]
                        filters=w, # [filter_height, filter_width, in_channels, out_channels]
                        strides=strides, 
                        padding=padding,
                        data_format=data_format) # [batch, out_height, out_width, out_channels]

    conv_shape = tuple(conv.shape)

    b_shape = (conv_shape[3],)
    b = variables.create_or_get_variable(name=f'{name}__b', shape=b_shape, dtype=dtype, initializer=bias_initializer)

    z = conv + b

    output = activation_fn(z)

    return output 





