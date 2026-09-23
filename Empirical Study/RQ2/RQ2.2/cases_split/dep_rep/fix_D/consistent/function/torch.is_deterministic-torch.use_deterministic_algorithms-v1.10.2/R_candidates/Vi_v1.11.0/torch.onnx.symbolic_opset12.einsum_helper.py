def einsum_helper(g, equation, tensors):
    if not tensors:
        raise RuntimeError("Einsum inputs are empty.")
    # ONNX does not support bool for Einsum inputs.
    if tensors[0].type().scalarType() == "Bool":
        tensors = [g.op("Cast", tensor, to_i=sym_help.cast_pytorch_to_onnx["Long"]) for tensor in tensors]
        return g.op("Cast", g.op("Einsum", *tensors, equation_s=equation), to_i=sym_help.cast_pytorch_to_onnx["Bool"])
    else:
        return g.op("Einsum", *tensors, equation_s=equation)
