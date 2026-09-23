def _rebuild_from_type_v2(func, new_type, args, state):
    if new_type is Tensor:
        return func(*args)

    ret = func(*args).as_subclass(new_type)
    # Tensor does define __setstate__ even though it doesn't define
    # __getstate__. So only use __setstate__ if it is NOT the one defined
    # on Tensor
    if getattr(ret.__class__, "__setstate__", Tensor.__setstate__) is not Tensor.__setstate__:
        ret.__setstate__(state)
    else:
        if isinstance(state, tuple):
            if not len(state) == 2:
                raise RuntimeError(f"Invalid serialized state: {state}")
            dict_state = state[0]
            slots_state = state[1]
        else:
            dict_state = state
            slots_state = None

        for k, v in dict_state.items():
            setattr(ret, k, v)

        if slots_state:
            for k, v in slots_state.items():
                setattr(ret, k, v)
    return ret
