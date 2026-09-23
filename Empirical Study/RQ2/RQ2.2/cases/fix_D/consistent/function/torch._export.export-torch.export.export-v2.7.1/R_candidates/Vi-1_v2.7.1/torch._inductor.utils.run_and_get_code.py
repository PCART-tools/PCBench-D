def run_and_get_code(
    fn: Callable[P, _T],
    *args: P.args,
    **kwargs: P.kwargs,
) -> tuple[_T, list[str]]:
    from .graph import GraphLowering

    source_codes: list[str] = []

    def save_output_code(code: str) -> None:
        source_codes.append(code)

    with mock.patch.object(GraphLowering, "save_output_code", save_output_code):
        torch._dynamo.reset()
        result = fn(*args, **kwargs)
    return result, source_codes
