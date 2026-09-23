def _get_module_type_filter(tp: Callable):
    """Get the module_type_filter function for a given module type, the filter accepts
    a node and checks if the node comes from a module that has certain module type

    For example:
        node: linear_op = call_function[...](...)  # comes from a module with type Block -> Sub -> Linear


    >> module_type_filter = _get_module_type_filter(Sub)  # submodule with type `Sub`, under the `Block` submodule
    >> print(module_type_filter(node))
    True  # the node is from the submodule `Sub` (same for `Block` and `Linear` as well)
    """

    tp_str = tp.__module__ + "." + tp.__qualname__

    def module_type_filter(n: Node) -> bool:
        # example: {
        #     'L__self___sub': ("L['self'].sub", <class '....Sub'>),
        #     'L__self___sub_linear': ("L['self'].sub.linear", <class 'torch.nn.modules.linear.Linear'>)
        # }
        nn_module_stack = n.meta.get("nn_module_stack", {})
        types = []
        for _, t in nn_module_stack.values():
            # export() returns str, but older APIs (e.g. capture_pre_autograd_graph)
            # return type. Handle both cases.
            if isinstance(t, type):
                t = t.__module__ + "." + t.__qualname__
            types.append(t)
        return tp_str in types

    return module_type_filter
