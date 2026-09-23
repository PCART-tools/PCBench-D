def tracing_with_real(x: torch.ScriptObject) -> bool:
    if not hasattr(x, "tracing_mode"):
        return False

    assert x.tracing_mode() in [
        "real",
        "fake",
    ], f"tracing_mode can be either real or fake but got {x.tracing_mode()}"
    return x.tracing_mode() == "real"
