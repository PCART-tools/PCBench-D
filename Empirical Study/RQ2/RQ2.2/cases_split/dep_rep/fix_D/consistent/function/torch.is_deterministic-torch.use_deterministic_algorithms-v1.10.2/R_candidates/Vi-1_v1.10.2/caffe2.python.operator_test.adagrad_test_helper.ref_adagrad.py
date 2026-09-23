def ref_adagrad(
    param_in,
    mom_in,
    grad,
    lr,
    epsilon,
    using_fp16=False,
    output_effective_lr=False,
    output_effective_lr_and_update=False,
    decay=1.0,
    row_wise=False,
    weight_decay=0.0,
    counter_halflife=-1,
    count=None,  # only used when counter_halflife != -1
):
    mom_in_f32 = mom_in
    param_in_f32 = param_in
    if using_fp16:
        mom_in_f32 = mom_in.astype(np.float32)
        param_in_f32 = param_in.astype(np.float32)

    if count and count > 0 and counter_halflife > 0:
        weight_decay *= counter_halflife / count
    grad_temp = grad + weight_decay * param_in_f32
    if row_wise:
        mom_out = decay * mom_in_f32 + np.mean(np.square(grad_temp))
    else:
        mom_out = decay * mom_in_f32 + np.square(grad_temp)
    effective_lr = lr / (np.sqrt(mom_out) + epsilon)
    grad_adj = effective_lr * grad_temp
    param_out = param_in_f32 + grad_adj

    if output_effective_lr_and_update:
        if using_fp16:
            return (
                param_out.astype(np.float16),
                mom_out.astype(np.float16),
                effective_lr.astype(np.float16),
                grad_adj.astype(np.float16),
            )
        else:
            return (
                param_out.astype(np.float32),
                mom_out.astype(np.float32),
                effective_lr.astype(np.float32),
                grad_adj.astype(np.float32),
            )
    elif output_effective_lr:
        if using_fp16:
            return (
                param_out.astype(np.float16),
                mom_out.astype(np.float16),
                effective_lr.astype(np.float16),
            )
        else:
            return (
                param_out.astype(np.float32),
                mom_out.astype(np.float32),
                effective_lr.astype(np.float32),
            )

    if using_fp16:
        return (param_out.astype(np.float16), mom_out.astype(np.float16))
    else:
        return (param_out.astype(np.float32), mom_out.astype(np.float32))
