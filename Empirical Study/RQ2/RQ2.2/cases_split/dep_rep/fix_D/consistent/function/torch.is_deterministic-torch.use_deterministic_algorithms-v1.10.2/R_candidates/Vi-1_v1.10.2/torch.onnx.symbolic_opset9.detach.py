def detach(g, input):
    # Erase aten::detach nodes because ONNX is inference only
    return input
