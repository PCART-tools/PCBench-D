def _calculate_scale(query, scale):
    # TODO: Investigate why math.sqrt() isn't properly handled by Dynamo?
    softmax_scale = scale if scale is not None else torch.sym_sqrt(1.0 / query.size(-1))
    return softmax_scale
