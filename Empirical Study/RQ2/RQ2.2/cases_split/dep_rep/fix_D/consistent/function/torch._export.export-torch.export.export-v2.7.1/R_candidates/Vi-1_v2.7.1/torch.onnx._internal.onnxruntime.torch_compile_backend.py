@compatibility(is_backward_compatible=False)
def torch_compile_backend(
    graph_module: torch.fx.GraphModule,
    args,
    *,
    options: Optional[Union[OrtBackendOptions, Mapping[str, Any]]] = None,
):
    return OrtBackend.get_cached_instance_for_options(options)(graph_module, args)
