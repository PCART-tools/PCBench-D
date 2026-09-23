def make_foreach_pointwise(pw_fn, allow_alpha=False):
    def inner(*inputs: list[list[TensorBox]], alpha=1):
        realize_outputs = (
            len(V.graph.current_node.users) == 0
            or V.graph.current_node.target in inplace_foreach_ops
            or cur_node_has_non_foreach_users()
        )

        a_list_input = None
        for input in inputs:
            if isinstance(input, (list, tuple)):
                a_list_input = input
                break
        assert a_list_input is not None, (
            "at least one input must be a list to a foreach op"
        )

        # broadcast scalar inputs to match length of list inputs
        broadcast_inputs = []
        for input in inputs:
            if not isinstance(input, (list, tuple)):
                broadcast_inputs.append([input] * len(a_list_input))
            else:
                broadcast_inputs.append(input)

        groups = group_foreach_args(zip(*broadcast_inputs))

        outputs = [None] * len(a_list_input)
        for (device, use_foreach), group in groups.items():
            operation_list: list[str] = []
            for (
                output_ind,
                args,
            ) in group:
                if allow_alpha:
                    output = pw_fn(*args, alpha=alpha)
                else:
                    output = pw_fn(*args)

                outputs[output_ind] = output

                if (
                    V.graph.has_feature(device, BackendFeature.FOREACH)
                    and use_foreach
                    and realize_outputs
                ):
                    output.realize()
                    operation_list.append(output.get_operation_name())

            if operation_list:
                V.graph.register_operation_list(operation_list)

        assert all(x is not None for x in outputs)
        return outputs

    return inner
