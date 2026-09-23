def _convert_ts_to_export_experimental(traced_callable, args, kwargs=None):
    with _temp_disable_texpr_fuser():
        from torch.jit._trace import TopLevelTracedModule

        export_args, export_kwargs = _process_jit_trace_inputs_for_export(args, kwargs)

        if isinstance(traced_callable, (TopLevelTracedModule, torch._C.ScriptModule)):  # type: ignore[operator]
            return _export(
                traced_callable,
                export_args,
                export_kwargs,
                strict=False,
                _is_torch_jit_trace=True,
            ).module()

        elif isinstance(traced_callable, torch.ScriptMethod) and isinstance(
            traced_callable.owner(),  # type: ignore[operator]
            (torch._C.ScriptModule, torch.nn.Module),
        ):
            with patch_forward(traced_callable.owner(), traced_callable):  # type: ignore[operator]
                return _export(
                    traced_callable.owner(),  # type: ignore[operator]
                    export_args,
                    export_kwargs,
                    strict=False,
                    _is_torch_jit_trace=True,
                ).module()

        else:
            return _export(
                _WrapperModule(traced_callable),
                export_args,
                export_kwargs,
                strict=False,
                _is_torch_jit_trace=True,
            ).module()
