def _kl_div_log_target_impl(g, input, target):
    diff_ = sub(g, target, input)
    exp_ = exp(g, target)
    output = mul(g, exp_, diff_)
    return output
