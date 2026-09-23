def set_rnn_executor_config(rnn_op, num_threads=None, max_cuda_streams=None):
    from caffe2.proto import caffe2_pb2
    assert rnn_op.type in {'RecurrentNetwork', 'RecurrentNetworkGradient'}

    def add_arg(s, v):
        a = caffe2_pb2.Argument()
        a.name = "rnn_executor." + s
        a.i = v
        rnn_op.arg.extend([a])

    if num_threads is not None:
        add_arg('num_threads', num_threads)
    if max_cuda_streams is not None:
        add_arg('max_cuda_streams', max_cuda_streams)
