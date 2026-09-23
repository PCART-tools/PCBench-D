def module_inputs_torch_nn_Transformer(module_info, device, dtype, requires_grad, **kwargs):
    make_input = partial(make_tensor, device=device, dtype=dtype, requires_grad=requires_grad)
    samples = []
    # Samples below are for validating the no-batch-dim support.
    key_padding_masks = (None, torch.tensor([False, False, True], device=device, dtype=torch.bool))
    attn_masks = (None, torch.tensor([False, False, True], device=device, dtype=torch.bool).expand((3, 3)))
    for mask, key_padding_mask, norm_first in itertools.product(attn_masks, key_padding_masks, (True, False)):
        # Using same mask for tgt and memory
        src_mask , tgt_mask = (mask,) * 2
        src_key_padding_mask, tgt_key_padding_mask = (key_padding_mask,) * 2
        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(d_model=4, nhead=2, dim_feedforward=8,
                                                num_encoder_layers=1, num_decoder_layers=1,
                                                dropout=0.0, batch_first=True, norm_first=norm_first),
                forward_input=FunctionInput(
                    make_input(shape=(3, 4)), make_input(shape=(3, 4)), tgt_mask=tgt_mask, src_mask=src_mask,
                    tgt_key_padding_mask=tgt_key_padding_mask, src_key_padding_mask=src_key_padding_mask
                ),
                reference_fn=partial(no_batch_dim_reference_fn,
                                     batch_first=True,
                                     kwargs_to_batchify={'tgt_key_padding_mask': 0, 'src_key_padding_mask': 0}),
                desc='no_batch_dim_batch_first'
            ))

        samples.append(
            ModuleInput(
                constructor_input=FunctionInput(d_model=4, nhead=2, dim_feedforward=8,
                                                num_encoder_layers=1, num_decoder_layers=1,
                                                dropout=0.0, batch_first=False, norm_first=norm_first),
                forward_input=FunctionInput(
                    make_input(shape=(3, 4)), make_input(shape=(3, 4)), tgt_mask=tgt_mask, src_mask=src_mask,
                    tgt_key_padding_mask=tgt_key_padding_mask, src_key_padding_mask=src_key_padding_mask
                ),
                reference_fn=partial(no_batch_dim_reference_fn,
                                     batch_first=False,
                                     kwargs_to_batchify={'tgt_key_padding_mask': 0, 'src_key_padding_mask': 0}),
                desc='no_batch_dim'
            ))

    return samples
