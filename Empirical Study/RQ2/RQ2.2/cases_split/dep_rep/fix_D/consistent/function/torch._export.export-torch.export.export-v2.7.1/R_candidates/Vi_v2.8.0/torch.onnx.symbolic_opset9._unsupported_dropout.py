@_onnx_symbolic(
    "aten::alpha_dropout_",
    decorate=[symbolic_helper._apply_params("aten::alpha_dropout_")],
)  # See Note [Export inplace]
@_onnx_symbolic(
    "aten::feature_alpha_dropout_",
    decorate=[symbolic_helper._apply_params("aten::feature_alpha_dropout_")],
)
@_onnx_symbolic(
    "aten::feature_dropout_",
    decorate=[symbolic_helper._apply_params("aten::feature_dropout_")],
)
@_onnx_symbolic(
    "aten::feature_alpha_dropout",
    decorate=[symbolic_helper._apply_params("aten::feature_alpha_dropout")],
)
@_onnx_symbolic(
    "aten::alpha_dropout",
    decorate=[symbolic_helper._apply_params("aten::alpha_dropout")],
)
@_onnx_symbolic(
    "aten::feature_dropout",
    decorate=[symbolic_helper._apply_params("aten::feature_dropout")],
)
def _unsupported_dropout(name: str):
    @symbolic_helper.parse_args("v", "none", "b")
    def feature_dropout(g, input, p, train):
        # NB: In inference mode, FeatureDropout is exported as an identity op.
        if train:
            return symbolic_helper._unimplemented(name, "training mode", input)
        return input

    return feature_dropout
