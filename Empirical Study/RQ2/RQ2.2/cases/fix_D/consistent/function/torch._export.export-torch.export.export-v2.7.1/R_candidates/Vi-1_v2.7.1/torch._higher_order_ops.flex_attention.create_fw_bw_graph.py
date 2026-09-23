def create_fw_bw_graph(
    score_mod: Callable,
    index_values: tuple[Tensor, Tensor, Tensor, Tensor, Tensor],
    other_buffers: tuple[Tensor, ...],
) -> tuple[Callable, Callable]:
    # See Note:[HOP create fw_bw graph]

    # All of these imports need to be here in order to avoid circular dependencies
    from torch._dispatch.python import suspend_functionalization
    from torch._functorch.aot_autograd import AOTConfig, create_joint
    from torch._subclasses.fake_tensor import FakeTensor, FakeTensorMode
    from torch._subclasses.functional_tensor import disable_functional_mode
    from torch.fx.experimental.proxy_tensor import disable_proxy_modes_tracing

    dummy_aot_config = AOTConfig(
        fw_compiler=None,  # type: ignore[arg-type]
        bw_compiler=None,  # type: ignore[arg-type]
        partition_fn=None,  # type: ignore[arg-type]
        decompositions={},
        num_params_buffers=0,
        aot_id=0,
        keep_inference_input_mutations=False,
    )

    with suspend_functionalization(), disable_functional_mode():
        with disable_proxy_modes_tracing():

            def _from_fun(
                t: Union[Tensor, torch.SymInt, int]
            ) -> Union[Tensor, torch.SymInt, int]:
                if isinstance(t, torch.Tensor):
                    return torch.empty_strided(
                        t.size(),
                        t.stride(),
                        device=t.device,
                        dtype=t.dtype,
                        requires_grad=t.requires_grad,
                    )
                return t

            # If someone runs this hop under the default compiler backend ("eager")
            # Then this path will be run with the actual user inputs. We convert them
            # to fake tensors in order to not perform any actual compute.
            from torch._guards import detect_fake_mode

            fake_mode = detect_fake_mode(index_values)
            if fake_mode is None:
                fake_mode = FakeTensorMode(allow_non_fake_inputs=True)

            with fake_mode:
                unwrapped_score_mod_indexes = pytree.tree_map(_from_fun, index_values)
                unwrapped_other_buffers = pytree.tree_map(_from_fun, other_buffers)

            assert all(
                isinstance(t, (FakeTensor, int, torch.SymInt))
                for t in unwrapped_score_mod_indexes + unwrapped_other_buffers
            )

            example_flat_out = pytree.tree_map(
                _from_fun,
                score_mod(*unwrapped_score_mod_indexes, *unwrapped_other_buffers),
            )
            if not isinstance(example_flat_out, torch.Tensor):
                raise RuntimeError(
                    "Expected output of score_mod to be a tensor."
                    f"Got type {type(example_flat_out)}."
                )
            example_grad = _from_fun(example_flat_out)

        def joint_f(
            score: Tensor,
            b: Tensor,
            h: Tensor,
            m: Tensor,
            n: Tensor,
            example_grad: Tensor,
            *other_buffers: tuple[Tensor, ...],
        ) -> tuple[Tensor, ...]:
            def fw_with_masks(
                *args: tuple[Tensor, ...]
            ) -> tuple[tuple[Tensor], tuple[bool]]:
                fw_out = score_mod(*args)
                out_requires_grad = fw_out.requires_grad
                return ((fw_out,), (out_requires_grad,))

            joint = create_joint(fw_with_masks, aot_config=dummy_aot_config)
            args = [score, b, h, m, n] + list(other_buffers)
            optional_grad = [example_grad] if example_grad.requires_grad else []
            _, grads = joint(args, optional_grad)

            return grads

        joint_graph = make_fx(joint_f)(
            *unwrapped_score_mod_indexes, example_grad, *unwrapped_other_buffers
        )
        return score_mod, joint_graph
