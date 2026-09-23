def camel_case_to_snake_case(s: str) -> str:
    return re.sub(r"([A-Z])", r"_\1", s).lower()
