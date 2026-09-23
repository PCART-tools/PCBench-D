@register_decomposition(aten.binary_cross_entropy_with_logits)
@out_wrapper()
def binary_cross_entropy_with_logits(
    self, target, weight=None, pos_weight=None, reduction=Reduction.MEAN.value
):
    if pos_weight is not None:
        log_weight = (pos_weight - 1) * target + 1
        loss = (1 - target) * self - (log_weight * F.logsigmoid(self))
    else:
        loss = (1 - target) * self - F.logsigmoid(self)

    if weight is not None:
        loss = loss * weight

    return apply_loss_reduction(loss, reduction)
