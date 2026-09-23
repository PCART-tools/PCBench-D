def _fx_compile_mode_default() -> tuple[FxCompileMode, bool]:
    name = "TORCHINDUCTOR_FX_COMPILE_MODE"
    value = os.environ.get(name)
    if value is None:
        return FxCompileMode.NORMAL, False

    use_async = False
    if value.lower().startswith("async+"):
        use_async = True
        value = value[6:]

    try:
        value = value.upper()
        return FxCompileMode[value], use_async
    except KeyError:
        import logging

        log = logging.getLogger(__name__)
        log.error(
            "Invalid value of %s for %s. Expected one of %s. Using default.",
            value,
            name,
            ", ".join(sorted(repr(x) for x in FxCompileMode.__members__.keys())),
        )
        # Remove from the environment so subprocesses don't ALSO complain.
        os.environ.pop(name)
        return FxCompileMode.NORMAL, False
