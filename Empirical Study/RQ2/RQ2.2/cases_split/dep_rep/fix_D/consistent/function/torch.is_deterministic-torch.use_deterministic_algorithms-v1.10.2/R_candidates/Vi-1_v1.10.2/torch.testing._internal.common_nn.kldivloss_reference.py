def kldivloss_reference(input, target, reduction='mean'):
    safe_target = target * (target > 0).type_as(target)
    safe_target_log = (safe_target + (target <= 0).type_as(target)).log()
    result = safe_target * (safe_target_log - input)
    if reduction == 'mean':
        return result.mean()
    elif reduction == 'sum':
        return result.sum()
    elif reduction == 'batchmean' and result.dim() != 0:
        return result.sum() / result.size(0)
    return result
