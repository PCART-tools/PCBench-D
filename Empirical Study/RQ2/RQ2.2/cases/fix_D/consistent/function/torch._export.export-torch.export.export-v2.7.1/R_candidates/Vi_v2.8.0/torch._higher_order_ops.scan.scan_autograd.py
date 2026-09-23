@scan_op.py_autograd_impl
def scan_autograd(combine_fn, init, xs, additional_inputs):
    num_leaves_init = len(init)
    num_leaves_xs = len(xs)
    num_additional_inputs = len(additional_inputs)

    flat_out = ScanAutogradOp.apply(
        combine_fn,
        num_leaves_init,
        num_leaves_xs,
        num_additional_inputs,
        *(tuple(init) + tuple(xs) + additional_inputs),
    )
    return *flat_out[:num_leaves_init], *flat_out[num_leaves_init:]
