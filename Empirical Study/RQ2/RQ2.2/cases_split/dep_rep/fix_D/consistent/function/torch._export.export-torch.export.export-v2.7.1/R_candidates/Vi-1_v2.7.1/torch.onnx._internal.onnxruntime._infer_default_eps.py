def _infer_default_eps() -> Sequence[str]:
    # TODO: select a good default based on the capabilities of the host
    # e.g. DML on Windows, etc.
    return ["CPUExecutionProvider"]
