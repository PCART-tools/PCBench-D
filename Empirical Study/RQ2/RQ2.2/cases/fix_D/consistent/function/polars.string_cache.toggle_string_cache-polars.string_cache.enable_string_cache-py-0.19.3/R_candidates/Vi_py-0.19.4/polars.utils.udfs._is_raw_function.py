def _is_raw_function(function: Callable[[Any], Any]) -> tuple[str, str]:
    """Identify translatable calls that aren't wrapped inside a lambda/function."""
    try:
        func_module = function.__class__.__module__
        func_name = function.__name__

        # numpy function calls
        if func_module == "numpy" and func_name in _NUMPY_FUNCTIONS:
            return "np", f"{func_name}()"

        # python function calls
        elif func_module == "builtins":
            if func_name in _PYTHON_CASTS_MAP:
                return "builtins", f"cast(pl.{_PYTHON_CASTS_MAP[func_name]})"
            elif func_name == "loads":
                import json  # double-check since it is referenced via 'builtins'

                if function is json.loads:
                    return "json", "str.json_extract()"

    except AttributeError:
        pass

    return "", ""
