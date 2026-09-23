def logdet(g, input):
    from torch.onnx.symbolic_opset9 import log
    return log(g, linalg_det(g, input))
