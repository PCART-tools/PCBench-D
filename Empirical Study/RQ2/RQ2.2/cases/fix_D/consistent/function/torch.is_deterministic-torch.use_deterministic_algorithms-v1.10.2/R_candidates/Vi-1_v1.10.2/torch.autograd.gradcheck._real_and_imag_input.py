def _real_and_imag_input(fn, complex_inp_indices):
    # returns new functions that take real inputs instead of complex inputs and compute fn(x + 0 * 1j)
    # and f(x * 1j).
    def apply_to_c_inps(fn, fn_to_apply):
        def wrapped_fn(*inputs):
            new_inputs = list(inputs)
            for should_be_complex in complex_inp_indices:
                new_inputs[should_be_complex] = fn_to_apply(new_inputs[should_be_complex])
            return _as_tuple(fn(*new_inputs))
        return wrapped_fn
    return apply_to_c_inps(fn, lambda x: x + 0 * 1j), apply_to_c_inps(fn, lambda x: x * 1j)
