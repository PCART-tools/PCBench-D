def unregister_custom_op_symbolic(symbolic_name, opset_version):
    from torch.onnx import utils
    utils.unregister_custom_op_symbolic(symbolic_name, opset_version)
