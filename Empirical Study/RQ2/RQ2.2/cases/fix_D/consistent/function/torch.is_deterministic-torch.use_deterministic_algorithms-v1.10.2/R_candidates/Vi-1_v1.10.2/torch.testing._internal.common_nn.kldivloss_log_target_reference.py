def kldivloss_log_target_reference(input, target, reduction='mean'):
    result = torch.exp(target) * (target - input)
    if reduction == 'mean':
        return result.mean()
    elif reduction == 'sum':
        return result.sum()
    elif reduction == 'batchmean' and result.dim() != 0:
        return result.sum() / result.size(0)
    return result
