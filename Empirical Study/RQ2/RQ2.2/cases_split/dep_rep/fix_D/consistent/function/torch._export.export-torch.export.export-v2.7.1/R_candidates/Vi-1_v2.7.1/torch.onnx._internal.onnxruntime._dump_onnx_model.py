def _dump_onnx_model(
    model_string: bytes, graph_module: Optional[torch.fx.GraphModule] = None
) -> str:
    """Stores the onnx model into a file.
    The name is "{ONNXRT_DUMP_PATH}{N}.onnx"
    where *N* is the number of files already stored with
    this prefix.
    If graph_module is not None, the graph is stored as a string with
    the same filename except the extension (.txt).
    """
    prefix = os.environ.get("ONNXRT_DUMP_PATH", None)
    if not prefix:
        return ""
    n = _dumped_onnx_model.get(prefix, -1) + 1
    filename = f"{prefix}{n}.onnx"
    with open(filename, "wb") as f:
        f.write(model_string)
    _dumped_onnx_model[prefix] = n
    if graph_module is not None:
        filename_txt = f"{prefix}{n}.txt"
        with open(filename_txt, "w", encoding="utf-8") as f:
            f.write(str(graph_module.graph))
    return filename
