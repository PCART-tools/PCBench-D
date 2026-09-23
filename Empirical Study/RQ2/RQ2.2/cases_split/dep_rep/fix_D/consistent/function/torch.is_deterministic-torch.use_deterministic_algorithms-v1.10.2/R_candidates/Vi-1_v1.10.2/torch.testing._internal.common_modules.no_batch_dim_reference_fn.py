def no_batch_dim_reference_fn(m, p, *args, **kwargs):
    """Reference function for modules supporting no batch dimensions.

    The module is passed the input and target in batched form with a single item.
    The output is squeezed to compare with the no-batch input.
    """
    single_batch_input_args = [input.unsqueeze(0) for input in args]
    with freeze_rng_state():
        return m(*single_batch_input_args).squeeze(0)
