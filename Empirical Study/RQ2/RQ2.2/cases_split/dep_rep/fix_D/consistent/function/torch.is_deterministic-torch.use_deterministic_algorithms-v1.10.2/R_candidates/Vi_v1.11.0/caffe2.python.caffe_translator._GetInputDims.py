def _GetInputDims(caffe_net):
    input_dims = []
    if caffe_net.input_dim:
        input_dims = caffe_net.input_dim
    elif caffe_net.input_shape:
        input_dims = caffe_net.input_shape[0].dim
    elif caffe_net.layer[0].input_param.shape:
        # getting input dimension from first layer
        input_dims = caffe_net.layer[0].input_param.shape[0].dim
    return input_dims
