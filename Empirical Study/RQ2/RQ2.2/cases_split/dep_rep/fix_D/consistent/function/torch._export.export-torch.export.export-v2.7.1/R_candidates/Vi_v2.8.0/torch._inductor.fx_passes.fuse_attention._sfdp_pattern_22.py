def _sfdp_pattern_22(query, key, value, attn_mask):
    # for T5 with inplace add and return key and value
    query = query.permute([0, 2, 1, 3])
    key = key.permute([0, 2, 1, 3])
    value = value.permute([0, 2, 1, 3])
    score = torch.matmul(query, key.permute(0, 1, 3, 2))
    masked_score = score + attn_mask
    score = masked_score.type_as(query)
    viewd_score1 = score.view(
        score.size(0) * score.size(1), score.size(2), score.size(3)
    )
    viewd_score2 = viewd_score1.view(
        score.size(0), score.size(1), score.size(2), score.size(3)
    )
    return viewd_score2.float().softmax(dim=-1).type_as(query).matmul(value), key, value
