def create_fw_bw_graph(f, num_mapped_args, *args):
    mapped_xs = args[:num_mapped_args]
    pos_args = args[num_mapped_args:]

    # See Note [HOP create fw_bw graph] in create_fw_bw_graph in utils.py

    with suspend_functionalization(), disable_functional_mode():
        with disable_proxy_modes_tracing():
            unwrapped_mapped_xs = pytree.tree_map(_from_fun, mapped_xs)
            example_xs = _unstack_pytree(unwrapped_mapped_xs)[0]

            example_pos_args = [
                _from_fun(arg) if isinstance(arg, torch.Tensor) else arg
                for arg in pos_args
            ]
            example_flat_out = pytree.tree_map(
                _from_fun, f(*example_xs, *example_pos_args)
            )
            if any(
                not isinstance(out, torch.Tensor)
                for out in example_flat_out
                if out is not None
            ):
                raise RuntimeError(
                    "Expect outputs of map only contains tensors or None. "
                    f"Got types {[type(out) for out in example_flat_out]}."
                )
            example_grad = [_from_fun(out) for out in example_flat_out]

            fw_graph = make_fx(f)(*example_xs, *example_pos_args)

        from torch._functorch.aot_autograd import AOTConfig, create_joint

        dummy_aot_config = AOTConfig(
            fw_compiler=None,  # type: ignore[arg-type]
            bw_compiler=None,  # type: ignore[arg-type]
            partition_fn=None,  # type: ignore[arg-type]
            decompositions={},
            num_params_buffers=0,
            aot_id=0,
            keep_inference_input_mutations=False,
        )

        def joint_f(*example_args):
            joint_mapped_args = example_args[:joint_num_mapped]
            args = example_args[joint_num_mapped:]

            mapped_input = joint_mapped_args[:num_mapped_args]
            mapped_grads = joint_mapped_args[num_mapped_args:]

            joint = create_joint(prepare_fw_with_masks(f), aot_config=dummy_aot_config)
            _, grads = joint(
                list(mapped_input) + list(args),
                [
                    grad
                    for grad in mapped_grads
                    if grad is not None and grad.requires_grad
                ],
            )

            # In order to keep map functional for backward graph,
            # we clone outputs that are aliasing inputs
            maybe_clone = clone_outputs_aliasing_inputs(example_args)

            return pytree.tree_map(maybe_clone, grads)

        joint_num_mapped = len(example_grad) + len(example_xs)
        joint_graph = make_fx(joint_f)(*example_xs, *example_grad, *example_pos_args)
        return fw_graph, joint_graph
