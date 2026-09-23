def get_multiheadattn(device: torch.device) -> GetterReturnType:
    # From https://github.com/pytorch/text/blob/master/test/data/test_modules.py#L10
    embed_dim, nhead, tgt_len, src_len, bsz = 10, 5, 6, 10, 64
    # Build torchtext MultiheadAttention module
    in_proj = models.InProjContainer(torch.nn.Linear(embed_dim, embed_dim, bias=False),
                                     torch.nn.Linear(embed_dim, embed_dim, bias=False),
                                     torch.nn.Linear(embed_dim, embed_dim, bias=False))

    model = models.MultiheadAttentionContainer(nhead, in_proj,
                                               models.ScaledDotProduct(),
                                               torch.nn.Linear(embed_dim, embed_dim, bias=False))
    model.to(device)
    params, names = extract_weights(model)

    query = torch.rand((tgt_len, bsz, embed_dim), device=device)
    key = value = torch.rand((src_len, bsz, embed_dim), device=device)
    attn_mask_2D = torch.randint(0, 2, (tgt_len, src_len), device=device).to(torch.bool)
    bias_k = bias_v = torch.rand((1, 1, embed_dim), device=device)

    attn_mask = torch.stack([attn_mask_2D] * (bsz * nhead))
    bias_k = bias_k.repeat(1, bsz, 1).reshape(1, bsz * nhead, -1)
    bias_v = bias_v.repeat(1, bsz, 1).reshape(1, bsz * nhead, -1)

    def forward(*new_params: Tensor) -> Tensor:
        load_weights(model, names, new_params)
        mha_output, attn_weights = model(query, key, value, attn_mask=attn_mask, bias_k=bias_k, bias_v=bias_v)

        # Don't test any specific loss, just backprop ones for both outputs
        loss = mha_output.sum() + attn_weights.sum()

        return loss

    return forward, params
