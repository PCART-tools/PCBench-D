def unimplemented_v2(
    gb_type: str,
    context: str,
    explanation: str,
    hints: list[str],
    *,
    from_exc: Any = _NOTHING,
    log_warning: bool = False,
) -> NoReturn:
    """
    Called within dynamo to cause a graph break.
    Args:
        gb_type: Context-free graph break type. It should be a short string without any
                 information specific to the tracing context (i.e. no dynamically-generated strings)
        context: Developer context for the graph break. It can contain tracing context/dynamic strings.
        explanation: User-facing context-dependent explanation for the graph break. Can be dynamic.
        hints: List of user-facing hints for the graph break.
    """

    msg = format_graph_break_message(gb_type, context, explanation, hints)
    if log_warning:
        log.warning(msg)
    if from_exc is not _NOTHING:
        raise Unsupported(msg) from from_exc
    raise Unsupported(msg)
