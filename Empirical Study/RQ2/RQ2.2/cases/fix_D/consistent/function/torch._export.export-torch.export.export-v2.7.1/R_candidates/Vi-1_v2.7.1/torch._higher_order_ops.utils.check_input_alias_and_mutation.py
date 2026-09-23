def check_input_alias_and_mutation(
    gm: torch.fx.GraphModule,
    fake_args: list[FakeTensor],
) -> tuple[list[int], dict[int, int], dict[int, int], dict[int, int]]:
    with disable_proxy_modes_tracing():
        """This function returns mutated inputs, inp-inp alias, inp-out alias, out-out alias
        in the graph module gm. It checks whether input tensor versions have
        changed after run gm once to detect mutation and checks tensor storage
        to detect alias.
        """
        from torch._prims_common import clone_preserve_strides

        def _tensor_version(t) -> Optional[int]:
            if isinstance(t, torch.Tensor):
                assert isinstance(t, FakeTensor), "Only fake tensor is allowed"
                return t._version
            return None

        def _tensor_storage(t) -> StorageWeakRef:
            return StorageWeakRef(t._typed_storage())

        # Clone the fake args to avoid mutating the original fake args
        with ExitStack() as ctx_stack:
            # We need to temporarily turn inference_mode off because
            # under inference mode, tensor version counter is not tracked.
            ctx_stack.enter_context(torch.inference_mode(False))
            cloned = [
                clone_preserve_strides(arg) if isinstance(arg, torch.Tensor) else arg
                for arg in fake_args
            ]
            before = [_tensor_version(arg) for arg in cloned]
            outputs = _maybe_fake_prop_ignore_unbacked(gm, cloned)
            outputs = [outputs] if not isinstance(outputs, (list, tuple)) else outputs
            after = [_tensor_version(arg) for arg in cloned]
            mutated_inputs = [
                i for i, (v1, v2) in enumerate(zip(before, after)) if v1 != v2
            ]
        # We need to analyze the original fake_args to detect
        # inp-inp alias.
        inp_storage_map = {
            _tensor_storage(inp): i
            for i, inp in enumerate(fake_args)
            if isinstance(inp, torch.Tensor)
        }
        inp_inp_alias_map = {
            i: inp_storage_map[_tensor_storage(inp)]
            for i, inp in enumerate(fake_args)
            if isinstance(inp, torch.Tensor)
            and inp_storage_map[_tensor_storage(inp)] != i
        }
        out_storage_map = {
            _tensor_storage(out): i
            for i, out in enumerate(outputs)
            if isinstance(out, torch.Tensor)
        }
        out_out_alias_map = {
            i: out_storage_map[_tensor_storage(out)]
            for i, out in enumerate(outputs)
            if isinstance(out, torch.Tensor)
            and out_storage_map[_tensor_storage(out)] != i
        }
        inp_out_alias_map = {
            i: out_storage_map[_tensor_storage(inp)]
            for i, inp in enumerate(cloned)
            if isinstance(inp, torch.Tensor) and _tensor_storage(inp) in out_storage_map
        }
        return mutated_inputs, inp_inp_alias_map, inp_out_alias_map, out_out_alias_map
