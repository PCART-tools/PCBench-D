def _export_to_torch_ir(
    f: Callable,
    args: tuple[Any, ...],
    kwargs: Optional[dict[str, Any]] = None,
    dynamic_shapes: Optional[Union[dict[str, Any], tuple[Any], list[Any]]] = None,
    *,
    preserve_module_call_signature: tuple[str, ...] = (),
    disable_constraint_solver: bool = False,
    allow_complex_guards_as_runtime_asserts: bool = False,
    restore_fqn: bool = True,
    _log_export_usage: bool = True,
    same_signature: bool = True,
) -> torch.fx.GraphModule:
    """
    Traces either an nn.Module's forward function or just a callable with PyTorch
    operations inside and produce a torch.fx.GraphModule in torch IR.
    """

    if _log_export_usage:
        log_export_usage(event="export.private_api", flags={"_export_to_torch_ir"})

    if not isinstance(args, tuple):
        raise UserError(
            UserErrorType.INVALID_INPUT,
            f"Expecting `args` to be a tuple of example positional inputs, got {type(args)}",
        )

    kwargs = kwargs or {}
    combined_args = _combine_args(f, args, kwargs)
    _check_dynamic_shapes(combined_args, dynamic_shapes)
    with torch._dynamo.config.patch(dataclasses.asdict(DEFAULT_EXPORT_DYNAMO_CONFIG)):
        try:
            module_call_specs: dict[str, dict[str, pytree.TreeSpec]] = {}
            ctx = nullcontext()
            if not isinstance(f, torch.fx.GraphModule):
                ctx = _wrap_submodules(  # type: ignore[assignment]
                    f, preserve_module_call_signature, module_call_specs
                )
            with ctx, _ignore_backend_decomps():
                gm_torch_level, _ = torch._dynamo.export(
                    f,
                    dynamic_shapes=dynamic_shapes,  # type: ignore[arg-type]
                    assume_static_by_default=True,
                    tracing_mode="symbolic",
                    disable_constraint_solver=disable_constraint_solver,
                    # currently the following 2 flags are tied together for export purposes,
                    # but untangle for sake of dynamo export api
                    prefer_deferred_runtime_asserts_over_guards=True,
                    allow_complex_guards_as_runtime_asserts=allow_complex_guards_as_runtime_asserts,
                    _log_export_usage=_log_export_usage,
                    same_signature=same_signature,
                )(
                    *args,
                    **kwargs,
                )
        except (ConstraintViolationError, ValueRangeError) as e:
            raise UserError(UserErrorType.CONSTRAINT_VIOLATION, str(e))  # noqa: B904
        except GuardOnDataDependentSymNode as e:
            raise UserError(  # noqa: B904
                UserErrorType.ANTI_PATTERN,
                f"Consider annotating your code using torch._check*(). {str(e)}",
                case_name="constrain_as_size_example",
            )

    gm_torch_level.meta["module_call_specs"] = module_call_specs

    if isinstance(f, torch.nn.Module) and restore_fqn:
        _restore_state_dict(f, gm_torch_level)

    return gm_torch_level
