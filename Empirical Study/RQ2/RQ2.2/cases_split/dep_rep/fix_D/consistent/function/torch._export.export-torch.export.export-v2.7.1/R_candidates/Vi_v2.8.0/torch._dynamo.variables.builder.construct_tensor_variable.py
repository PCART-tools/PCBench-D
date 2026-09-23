def construct_tensor_variable(
    target_cls, tx, proxy, example_value, subclass_type, options
):
    """
    Actually construct a tensor variable after all the pre-processing from
    wrapping a pre-existing or newly created tensor value.
    """
    # NB: In most (all?) cases, this does not actually do a clone.
    # (WARNING: this means that if we mutate metadata on the fake
    # tensor, the stored example value will update too!)
    example_value = _clone_input(example_value, tx.fake_mode)
    set_example_value(proxy.node, example_value)
    # We bind the unbacked symints in sizes/trdies of tensor lazily.
    # So that subgraphs can access the unbacked symbol's proxy in parent graph
    # when lifting unbacked symbols of input tensors to subgraph inputs.
    # We do it lazily because the tensor may not be used in subgraphs.
    tx.output.current_tracer.track_unbacked_symbols(example_value, proxy)
    specialized_props = target_cls.specialize(example_value)
    # TODO: not sure about this fake mode test
    if (
        isinstance(example_value, torch._subclasses.fake_tensor.FakeTensor)
        and example_value.fake_mode is tx.fake_mode
    ):
        if subclass_type:
            tensor_type = subclass_type
        elif isinstance(example_value, torch.nn.Parameter):
            tensor_type = torch.nn.Parameter
        elif isinstance(example_value, torch.nn.Buffer):
            tensor_type = torch.nn.Buffer
        else:
            tensor_type = torch.Tensor
        specialized_props["class_type"] = tensor_type

    options.update(specialized_props)
    return target_cls(proxy, **options)
