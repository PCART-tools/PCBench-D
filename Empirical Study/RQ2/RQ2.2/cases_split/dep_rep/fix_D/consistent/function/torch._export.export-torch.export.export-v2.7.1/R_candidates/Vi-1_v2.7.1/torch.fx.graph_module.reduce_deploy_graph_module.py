@compatibility(is_backward_compatible=True)
def reduce_deploy_graph_module(
    importer: PackageImporter, body: dict[Any, Any], import_block: str
) -> torch.nn.Module:
    ns = {}
    ns["__builtins__"] = importer.patched_builtins
    fn_src = body.get("_code")
    assert fn_src is not None
    forward = _forward_from_src(import_block + fn_src, ns)
    return _deserialize_graph_module(forward, body)
