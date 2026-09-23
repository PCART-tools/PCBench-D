@typing_extensions.deprecated(
    "torch.onnx.verification.* is deprecated. Consider using torch.onnx.export(..., dynamo=True) "
    "and use ONNXProgram to test the ONNX model"
)
def find_mismatch(
    model: torch.nn.Module | torch.jit.ScriptModule,
    input_args: tuple[Any, ...],
    do_constant_folding: bool = True,
    training: _C_onnx.TrainingMode = _C_onnx.TrainingMode.EVAL,
    opset_version: int | None = None,
    keep_initializers_as_inputs: bool = True,
    verbose: bool = False,
    options: VerificationOptions | None = None,
) -> GraphInfo:
    r"""Find all mismatches between the original model and the exported model.

    .. deprecated:: 2.7
        Consider using ``torch.onnx.export(..., dynamo=True)`` and use the returned
        ``ONNXProgram`` to test the ONNX model.

    Experimental. The API is subject to change.

    This tool helps debug the mismatch between the original PyTorch model and exported
    ONNX model. It binary searches the model graph to find the minimal subgraph that
    exhibits the mismatch.

    Args:
        model: The model to be exported.
        input_args: The input arguments to the model.
        do_constant_folding: Same as `do_constant_folding` in :func:`torch.onnx.export`.
        training: Same as `training` in :func:`torch.onnx.export`.
        opset_version: Same as `opset_version` in :func:`torch.onnx.export`.
        keep_initializers_as_inputs: Same as `keep_initializers_as_inputs` in :func:`torch.onnx.export`.
        verbose: Same as `verbose` in :func:`torch.onnx.export`.
        options: The options for the mismatch verification.

    Returns:
        A GraphInfo object that contains the mismatch information.

    Example::

        >>> import torch
        >>> import torch.onnx.verification
        >>> torch.manual_seed(0)
        >>> opset_version = 15
        >>> # Define a custom symbolic function for aten::relu.
        >>> # The custom symbolic function is incorrect, which will result in mismatches.
        >>> def incorrect_relu_symbolic_function(g, self):
        ...     return self
        >>> torch.onnx.register_custom_op_symbolic(
        ...     "aten::relu",
        ...     incorrect_relu_symbolic_function,
        ...     opset_version=opset_version,
        ... )
        >>> class Model(torch.nn.Module):
        ...     def __init__(self) -> None:
        ...         super().__init__()
        ...         self.layers = torch.nn.Sequential(
        ...             torch.nn.Linear(3, 4),
        ...             torch.nn.ReLU(),
        ...             torch.nn.Linear(4, 5),
        ...             torch.nn.ReLU(),
        ...             torch.nn.Linear(5, 6),
        ...         )
        ...     def forward(self, x):
        ...         return self.layers(x)
        >>> # xdoctest: +REQUIRES(env:TORCH_DOCTEST_ONNX)
        >>> graph_info = torch.onnx.verification.find_mismatch(
        ...     Model(),
        ...     (torch.randn(2, 3),),
        ...     opset_version=opset_version,
        ... )
        ===================== Mismatch info for graph partition : ======================
        ================================ Mismatch error ================================
        Tensor-likes are not close!
        Mismatched elements: 12 / 12 (100.0%)
        Greatest absolute difference: 0.2328854203224182 at index (1, 2) (up to 1e-07 allowed)
        Greatest relative difference: 0.699536174352349 at index (1, 3) (up to 0.001 allowed)
        ==================================== Tree: =====================================
        5 X   __2 X    __1 \u2713
        id:  |  id: 0 |  id: 00
             |        |
             |        |__1 X (aten::relu)
             |           id: 01
             |
             |__3 X    __1 \u2713
                id: 1 |  id: 10
                      |
                      |__2 X     __1 X (aten::relu)
                         id: 11 |  id: 110
                                |
                                |__1 \u2713
                                   id: 111
        =========================== Mismatch leaf subgraphs: ===========================
        ['01', '110']
        ============================= Mismatch node kinds: =============================
        {'aten::relu': 2}

    """
    if options is None:
        options = VerificationOptions()
    if opset_version is None:
        opset_version = _constants.ONNX_DEFAULT_OPSET
    """From aten graph, do binary search on graph partition to find operator export discrepancy."""
    # TODO: Copied from utils.py `export` until `_optimize_graph`.
    if training == torch.onnx.TrainingMode.TRAINING:
        model.train()
    elif training == torch.onnx.TrainingMode.EVAL:
        model.eval()
    with torch.no_grad():
        inputs_for_export = _prepare_input_for_export(input_args, {})
        args = utils._decide_input_format(model, inputs_for_export)

        model = utils._pre_trace_quant_model(model, args)
        graph, params, _torch_out, _module = utils._create_jit_graph(model, args)
        params_dict = utils._get_named_param_dict(graph, params)

        utils._apply_friendly_debug_names(graph, params_dict)

        graph_info = GraphInfo(
            graph,
            input_args,
            params_dict,
            _experimental.ExportOptions(
                do_constant_folding=do_constant_folding,
                training=training,
                opset_version=opset_version,
                keep_initializers_as_inputs=keep_initializers_as_inputs,
                verbose=verbose,
            ),
        )
        graph_info.find_mismatch(options)
        graph_info.pretty_print_mismatch()
        graph_info.pretty_print_tree()

        return graph_info
