def no_batch_dim_reference_criterion_fn(m, *args, **kwargs):
    """Reference function for criterion supporting no batch dimensions."""
    output = no_batch_dim_reference_fn(m, *args, **kwargs)
    reduction = get_reduction(m)
    if reduction == 'none':
        return output.squeeze(0)
    # reduction is 'sum' or 'mean' which results in a 0D tensor
    return output
