def unimplemented(
    msg: str, *, from_exc: Any = _NOTHING, case_name: Optional[str] = None
) -> NoReturn:
    assert msg != os.environ.get("BREAK", False)
    if from_exc is not _NOTHING:
        raise Unsupported(msg, case_name=case_name) from from_exc
    raise Unsupported(msg, case_name=case_name)
