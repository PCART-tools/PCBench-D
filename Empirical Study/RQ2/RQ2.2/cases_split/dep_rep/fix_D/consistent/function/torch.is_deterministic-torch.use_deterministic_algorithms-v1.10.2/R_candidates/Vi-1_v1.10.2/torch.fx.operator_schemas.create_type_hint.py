@compatibility(is_backward_compatible=False)
def create_type_hint(x):
    try:
        if isinstance(x, list) or isinstance(x, tuple):
            # todo(chilli): Figure out the right way for mypy to handle this
            if isinstance(x, list):
                def ret_type(x):
                    return List[x]  # type: ignore[valid-type]
            else:
                def ret_type(x):
                    return Tuple[x, ...]
            if len(x) == 0:
                return ret_type(Any)
            base_type = x[0]
            for t in x:
                if issubclass(t, base_type):
                    continue
                elif issubclass(base_type, t):
                    base_type = t
                else:
                    return ret_type(Any)
            return ret_type(base_type)
    except Exception as e:
        # We tried to create a type hint for list but failed.
        torch.warnings.warn(f"We were not able to successfully create type hint from the type {x}")
        pass
    return x
