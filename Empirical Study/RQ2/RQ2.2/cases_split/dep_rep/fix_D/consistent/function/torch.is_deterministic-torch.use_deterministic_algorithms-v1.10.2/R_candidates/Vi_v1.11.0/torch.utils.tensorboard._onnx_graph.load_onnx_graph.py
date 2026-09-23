def load_onnx_graph(fname):
    import onnx
    m = onnx.load(fname)
    g = m.graph
    return parse(g)
