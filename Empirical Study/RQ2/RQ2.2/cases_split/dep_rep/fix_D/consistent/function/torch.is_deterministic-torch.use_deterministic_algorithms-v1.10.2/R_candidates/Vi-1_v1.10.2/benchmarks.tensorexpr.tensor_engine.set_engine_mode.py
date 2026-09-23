def set_engine_mode(mode):
    global tensor_engine
    if mode == "tf":
        from . import tf_engine

        tensor_engine = tf_engine.TensorFlowEngine()
    elif mode == "pt":
        from . import pt_engine

        tensor_engine = pt_engine.TorchTensorEngine()
    elif mode == "topi":
        from . import topi_engine

        tensor_engine = topi_engine.TopiEngine()
    elif mode == "relay":
        from . import relay_engine

        tensor_engine = relay_engine.RelayEngine()
    elif mode == "nnc":
        from . import nnc_engine

        tensor_engine = nnc_engine.NncEngine()
    else:
        raise ValueError("invalid tensor engine mode: %s" % (mode))
    tensor_engine.mode = mode
