def check_input_alias_and_mutation_return_outputs(
    gm: torch.fx.GraphModule,
    fake_args: Union[list[FakeTensor], tuple[FakeTensor, ...]],
) -> tuple[
    dict[int, int],
    dict[int, int],
    dict[int, int],
    list[int],
    Union[tuple[Any, ...], list[Any]],
]:
    # This function can be called under autograd, functional, proxy and fake tensor mode.
    # We need to return either a fake tensor or a real tensor depending on the mode.
    # to detect the input mutation/aliasing.
    with disable_proxy_modes_tracing(), disable_functional_mode(), suspend_functionalization():

        def _from_functional_tensor(t: torch.Tensor) -> torch.Tensor:
            if isinstance(t, FunctionalTensor) or torch._is_functional_tensor(t):
                return torch.empty_strided(
                    t.size(),
                    t.stride(),
                    dtype=t.dtype,
                    requires_grad=t.requires_grad,
                    device=t.device,
                )
            return t

        fake_args = pytree.tree_map_only(
            torch.Tensor, _from_functional_tensor, fake_args
        )
    # We want to disable active functional, proxy and fake modes if any.
    # to create a encapsulated environment for fake tensor prop
    with torch.utils._python_dispatch._disable_current_modes():
        """This function returns mutated inputs, inp-inp alias, inp-out alias, out-out alias
        in the graph module gm. It checks whether input tensor versions have
        changed after run gm once to detect mutation and checks tensor storage
        to detect alias.
        """

        def _tensor_version(t) -> Optional[int]:
            if isinstance(t, torch.Tensor):
                if not isinstance(t, FakeTensor):
                    raise RuntimeError("Only fake tensor is allowed")
                return t._version
            return None

        def _tensor_storage(t) -> StorageWeakRef:
            return StorageWeakRef(t._typed_storage())

        def _get_shape_env(
            fake_args,
        ) -> Optional[torch.fx.experimental.symbolic_shapes.ShapeEnv]:
            # detect_fake_mode requires there could be only one active fake mode. This
            # restricts the usage of this function because the global TracingContext
            # has a persistent fake mode but fake tensors can be created
            # outside of the tracing context (e.g. in testing).
            # Instead, we just look at fake_args fake tensor mode
            if len(fake_args) == 0:
                return torch.fx.experimental.symbolic_shapes.ShapeEnv()

            for arg in fake_args:
                if isinstance(arg, FakeTensor):
                    return arg.fake_mode.shape_env
            return None

        # Clone the fake args to avoid mutating the original fake args
        with ExitStack() as ctx_stack:
            # We need to re-use prev_fake_mode's shape env to resolve
            # the runtime assertions for unbacked symbols.
            new_fake_mode = torch._subclasses.FakeTensorMode(
                shape_env=_get_shape_env(fake_args),
                allow_non_fake_inputs=False,
            )
            # We need to temporarily turn inference_mode off because
            # under inference mode, tensor version counter is not tracked.
            no_inference_mode_ctx = torch.inference_mode(False)
            ctx_stack.enter_context(new_fake_mode)
            ctx_stack.enter_context(no_inference_mode_ctx)
            if new_fake_mode.shape_env is not None:
                ctx_stack.enter_context(
                    new_fake_mode.shape_env.ignore_fresh_unbacked_symbols()
                )

            # create new fake tensors in new fake mode to avoid mutating original tensors
            cloned = [
                torch.empty_strided(
                    arg.size(),
                    arg.stride(),
                    dtype=arg.dtype,
                    device=arg.device,
                    requires_grad=arg.requires_grad,
                    layout=arg.layout,
                )
                if isinstance(arg, torch.Tensor)
                else arg
                for arg in fake_args
            ]
            before = [_tensor_version(arg) for arg in cloned]
            outputs = gm(*cloned)
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
        return (
            inp_inp_alias_map,
            inp_out_alias_map,
            out_out_alias_map,
            mutated_inputs,
            outputs,
        )
