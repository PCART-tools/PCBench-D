def common_pre_export_passes(
    options: ResolvedExportOptions,
    original_model: torch.nn.Module | Callable,
    fx_module: torch.fx.GraphModule,
    fx_module_args: Sequence[Any],
):
    # TODO: Import here to prevent circular dependency
    from torch.onnx._internal.fx import passes

    # Apply decomposition table to the input graph.
    module = passes.Decompose(
        fx_module,
        options.decomposition_table,  # type: ignore[arg-type]
        enable_dynamic_axes=options.dynamic_shapes,
        allow_fake_constant=options.fake_context is not None,
    ).run(*fx_module_args)

    # ONNX does not support views and mutations.
    # Functionalize to get a semantically equivalent graph without mutations.
    module = passes.Functionalize(
        module,
        enable_dynamic_axes=options.dynamic_shapes,
        allow_fake_constant=options.fake_context is not None,
    ).run(*fx_module_args)

    # Input mutations are detected and distilled after `Functionalize` pass.
    # Remove them since ONNX inference does not need them.
    module = passes.RemoveInputMutation(module).run(*fx_module_args)

    # ONNX does not support concept of (implicit) type promotion.
    # Insert type casts explicitly where needed.
    module = passes.InsertTypePromotion(module).run()

    if isinstance(original_model, torch.nn.Module):
        module = passes.RestoreParameterAndBufferNames(module, original_model).run()

    # ONNX does not support None inputs. During graph building, all None inputs
    # are removed. Here we register this step to input adapter.
    options.fx_tracer.input_adapter.append_step(io_adapter.RemoveNoneInputStep())

    # NOTE: temp workaround for https://github.com/pytorch/pytorch/issues/99534
    # Dynamo doesn't support non-tensor inputs.
    options.fx_tracer.input_adapter.append_step(io_adapter.RemoveNonTensorInputStep())

    # ONNX does not support complex inputs. During graph building, all complex inputs
    # are converted to real representation inputs. Here we register this step to
    # input/output adapter.
    options.fx_tracer.input_adapter.append_step(
        io_adapter.ConvertComplexToRealRepresentationInputStep()
    )

    # ONNX can't represent collection types (e.g., dictionary, tuple of tuple of
    # tensor, etc), we flatten the collection and register each element as output.
    options.fx_tracer.output_adapter.append_step(io_adapter.FlattenOutputStep())

    # Output post-processing steps should happen after `FlattenOutputStep`.
    options.fx_tracer.output_adapter.append_step(
        io_adapter.ConvertComplexToRealRepresentationOutputStep()
    )

    return module
