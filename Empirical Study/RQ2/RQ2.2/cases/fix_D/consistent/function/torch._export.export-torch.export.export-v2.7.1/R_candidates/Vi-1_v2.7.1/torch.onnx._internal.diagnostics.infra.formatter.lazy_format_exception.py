def lazy_format_exception(exception: Exception) -> LazyString:
    return LazyString(
        lambda: "\n".join(
            (
                "```",
                *traceback.format_exception(
                    type(exception), exception, exception.__traceback__
                ),
                "```",
            )
        ),
    )
