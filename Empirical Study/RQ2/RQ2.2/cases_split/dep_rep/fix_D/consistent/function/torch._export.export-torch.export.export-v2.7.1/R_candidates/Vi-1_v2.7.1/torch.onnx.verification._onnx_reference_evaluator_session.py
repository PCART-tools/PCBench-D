def _onnx_reference_evaluator_session(model: str | io.BytesIO):
    try:
        import onnx
        from onnx import reference as onnx_reference  # type: ignore[attr-defined]
    except ImportError as exc:
        raise ImportError("onnx >= 1.13 is required for reference evaluator.") from exc

    proto = (
        onnx.load(model)  # type: ignore[attr-defined]
        if isinstance(model, str)
        else onnx.load_model_from_string(model.getvalue())  # type: ignore[attr-defined]
    )
    onnx_session = onnx_reference.ReferenceEvaluator(proto)
    return onnx_session
