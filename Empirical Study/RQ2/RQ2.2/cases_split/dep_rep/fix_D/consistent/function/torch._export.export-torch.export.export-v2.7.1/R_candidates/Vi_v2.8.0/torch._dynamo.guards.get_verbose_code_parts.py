def get_verbose_code_parts(
    code_parts: Union[str | list[str]], guard: Guard
) -> list[str]:
    if not isinstance(code_parts, list):
        code_parts = [code_parts]
    return [get_verbose_code_part(code_part, guard) for code_part in code_parts]
