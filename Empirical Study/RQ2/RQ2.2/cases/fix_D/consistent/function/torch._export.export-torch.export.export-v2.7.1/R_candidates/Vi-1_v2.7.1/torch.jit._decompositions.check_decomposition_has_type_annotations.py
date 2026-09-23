def check_decomposition_has_type_annotations(f):
    inspect_empty = inspect._empty  # type: ignore[attr-defined]
    sig = inspect.signature(f)
    for param in sig.parameters.values():
        assert (
            param.annotation != inspect_empty
        ), f"No signature on param {param.name} for function {f.name}"

    assert (
        sig.return_annotation != inspect_empty
    ), f"No return annotation for function {f.name}"
