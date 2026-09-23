def dynamo_export(
    model: torch.nn.Module | Callable,
    /,
    *model_args,
    export_options: ExportOptions | None = None,
    **model_kwargs,
) -> _onnx_program.ONNXProgram:
    """Export a torch.nn.Module to an ONNX graph.

    .. deprecated:: 2.7
        Please use ``torch.onnx.export(..., dynamo=True)`` instead.

    Args:
        model: The PyTorch model to be exported to ONNX.
        model_args: Positional inputs to ``model``.
        model_kwargs: Keyword inputs to ``model``.
        export_options: Options to influence the export to ONNX.

    Returns:
        An in-memory representation of the exported ONNX model.

    **Example 1 - Simplest export**
    ::

        class MyModel(torch.nn.Module):
            def __init__(self) -> None:
                super().__init__()
                self.linear = torch.nn.Linear(2, 2)

            def forward(self, x, bias=None):
                out = self.linear(x)
                out = out + bias
                return out


        model = MyModel()
        kwargs = {"bias": 3.0}
        args = (torch.randn(2, 2, 2),)
        onnx_program = torch.onnx.dynamo_export(model, *args, **kwargs).save(
            "my_simple_model.onnx"
        )

    **Example 2 - Exporting with dynamic shapes**
    ::

        # The previous model can be exported with dynamic shapes
        export_options = torch.onnx.ExportOptions(dynamic_shapes=True)
        onnx_program = torch.onnx.dynamo_export(
            model, *args, **kwargs, export_options=export_options
        )
        onnx_program.save("my_dynamic_model.onnx")


    By printing input dynamic dimensions we can see the input shape is no longer (2,2,2)
    ::

        >>> print(onnx_program.model_proto.graph.input[0])
        name: "arg0"
        type {
          tensor_type {
            elem_type: 1
            shape {
              dim {
                dim_param: "arg0_dim_0"
              }
              dim {
                dim_param: "arg0_dim_1"
              }
              dim {
                dim_param: "arg0_dim_2"
              }
            }
          }
        }
    """

    if export_options is not None:
        resolved_export_options = (
            export_options
            if isinstance(export_options, ResolvedExportOptions)
            else ResolvedExportOptions(export_options, model=model)
        )
    else:
        resolved_export_options = ResolvedExportOptions(ExportOptions(), model=model)

    _assert_dependencies(resolved_export_options)

    try:
        from torch._dynamo import config as _dynamo_config

        with _dynamo_config.patch(do_not_emit_runtime_asserts=True):
            return Exporter(
                options=resolved_export_options,
                model=model,
                model_args=model_args,
                model_kwargs=model_kwargs,
            ).export()
    except Exception as e:
        sarif_report_path = _DEFAULT_FAILED_EXPORT_SARIF_LOG_PATH
        resolved_export_options.diagnostic_context.dump(sarif_report_path)
        message = (
            f"Failed to export the model to ONNX. Generating SARIF report at '{sarif_report_path}'. "
            "SARIF is a standard format for the output of static analysis tools. "
            "SARIF logs can be loaded in VS Code SARIF viewer extension, "
            "or SARIF web viewer (https://microsoft.github.io/sarif-web-component/). "
            f"Please report a bug on PyTorch Github: {_PYTORCH_GITHUB_ISSUES_URL}"
        )
        raise errors.OnnxExporterError(message) from e
