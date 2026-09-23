def _apply_fc_weight_for_sum_match(
    model,
    input,
    dim_in,
    dim_out,
    scope,
    name,
):
    output = brew.fc(
        model,
        input,
        s(scope, name),
        dim_in=dim_in,
        dim_out=dim_out,
        axis=2,
    )
    output = model.net.Squeeze(
        output,
        output,
        dims=[0],
    )
    return output
