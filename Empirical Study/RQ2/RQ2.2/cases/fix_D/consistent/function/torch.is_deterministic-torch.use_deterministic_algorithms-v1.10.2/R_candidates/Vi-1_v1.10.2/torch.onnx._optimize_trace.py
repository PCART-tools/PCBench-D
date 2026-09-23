def _optimize_trace(graph, operator_export_type):
    from torch.onnx import utils
    return utils._optimize_graph(graph, operator_export_type)
