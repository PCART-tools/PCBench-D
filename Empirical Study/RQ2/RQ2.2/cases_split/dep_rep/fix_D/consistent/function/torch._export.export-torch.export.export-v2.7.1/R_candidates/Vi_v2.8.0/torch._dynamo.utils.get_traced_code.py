def get_traced_code() -> list[CodeType]:
    from torch._guards import TracingContext

    return TracingContext.get_traced_code()
