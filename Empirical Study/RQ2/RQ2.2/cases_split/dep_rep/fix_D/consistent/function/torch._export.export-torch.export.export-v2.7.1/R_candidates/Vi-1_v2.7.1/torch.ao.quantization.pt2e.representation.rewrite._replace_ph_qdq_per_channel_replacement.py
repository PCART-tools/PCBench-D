def _replace_ph_qdq_per_channel_replacement(gm: torch.fx.GraphModule):
    return _replace_literals_with_existing_placeholders(
        gm, exclude_literals=[-1], literal_to_ph_idx={1: 3, -128: 4, 127: 5}
    )
