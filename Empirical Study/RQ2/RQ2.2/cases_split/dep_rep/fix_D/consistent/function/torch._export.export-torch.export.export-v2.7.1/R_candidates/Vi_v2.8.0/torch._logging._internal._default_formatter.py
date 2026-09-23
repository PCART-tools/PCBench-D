def _default_formatter():
    fmt = os.environ.get(LOG_FORMAT_ENV_VAR, None)
    trace_id_filter = {
        item.strip()
        for item in os.environ.get(LOG_TRACE_ID_FILTER, "").split(",")
        if item.strip()
    }
    if fmt is None:
        return TorchLogsFormatter(trace_id_filter=trace_id_filter)
    else:
        if fmt in ("short", "basic"):
            fmt = logging.BASIC_FORMAT
        return logging.Formatter(fmt)
