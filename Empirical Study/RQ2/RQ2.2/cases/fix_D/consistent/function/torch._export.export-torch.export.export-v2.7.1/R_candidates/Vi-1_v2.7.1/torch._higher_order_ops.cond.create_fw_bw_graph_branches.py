def create_fw_bw_graph_branches(true_fn, false_fn, *operands):
    # See Note [HOP create fw_bw graph] in create_fw_bw_graph in utils.py

    with suspend_functionalization(), disable_functional_mode():
        with disable_proxy_modes_tracing():
            fw_inputs = pytree.tree_map(_from_fun, operands)

            fw_outputs_true = pytree.tree_map(
                _from_fun, _maybe_fake_prop_ignore_unbacked(true_fn, fw_inputs)
            )
            if any(
                not isinstance(out, torch.Tensor)
                for out in fw_outputs_true
                if out is not None
            ):
                raise RuntimeError(
                    "Expect outputs of true_fn to only contains tensors or None. "
                    f"Got types {[type(out) for out in fw_outputs_true]}."
                )
            fw_outputs_false = pytree.tree_map(
                _from_fun, _maybe_fake_prop_ignore_unbacked(false_fn, fw_inputs)
            )
            if any(
                not isinstance(out, torch.Tensor)
                for out in fw_outputs_false
                if out is not None
            ):
                raise RuntimeError(
                    "Expect outputs of false_fn to only contains tensors or None. "
                    f"Got types {[type(out) for out in fw_outputs_false]}."
                )

            # TODO: There is a major issue that the create_fw_bw in the higher_order_op is invoked twice:
            # Once in the forward path (as it should) and once in the backward path, where it shouldn't be called
            # If we can get rid of the second invokation, it would simplify this function
            fw_true_graph, joint_true_graph = create_fw_bw_graph(
                true_fn, False, fw_inputs, fw_outputs_true
            )
            fw_false_graph, joint_false_graph = create_fw_bw_graph(
                false_fn, False, fw_inputs, fw_outputs_false
            )

        return fw_true_graph, fw_false_graph, joint_true_graph, joint_false_graph
