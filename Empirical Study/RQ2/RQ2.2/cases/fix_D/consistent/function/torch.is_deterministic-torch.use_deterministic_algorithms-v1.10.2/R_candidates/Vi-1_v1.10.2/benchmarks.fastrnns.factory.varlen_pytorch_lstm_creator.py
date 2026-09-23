def varlen_pytorch_lstm_creator(**kwargs):
    rnn_utils = torch.nn.utils.rnn
    sequences, _, hidden, _, module = varlen_lstm_inputs(
        return_module=True, **kwargs)

    def forward(sequences, hidden):
        packed = rnn_utils.pack_sequence(sequences, enforce_sorted=False)
        out, new_hidden = module(packed, hidden)
        padded, lengths = rnn_utils.pad_packed_sequence(out)
        # XXX: It's more efficient to store the output in its padded form,
        # but that might not be conducive to loss computation.
        # Un-padding the output also makes the backward pass 2x slower...
        # return [padded[:lengths[i], i, :] for i in range(lengths.size(0))]
        return padded, new_hidden

    return ModelDef(
        inputs=[sequences, hidden],
        params=flatten_list(module.all_weights),
        forward=forward,
        backward_setup=lstm_backward_setup,
        backward=simple_backward)
