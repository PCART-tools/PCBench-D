def isinf(g, input):
    from torch.onnx.symbolic_opset9 import _cast_Double  # type: ignore[attr-defined]
    return g.op("IsInf", _cast_Double(g, input, False))
