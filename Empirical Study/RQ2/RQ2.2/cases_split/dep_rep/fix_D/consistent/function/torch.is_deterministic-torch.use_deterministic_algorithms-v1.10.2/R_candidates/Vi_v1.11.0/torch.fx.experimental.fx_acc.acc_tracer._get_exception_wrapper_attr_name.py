def _get_exception_wrapper_attr_name(exc_type: Type[Exception]) -> str:
    return f"_conditional_exception_wrapper_{exc_type.__name__}"
