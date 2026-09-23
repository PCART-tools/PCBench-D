def prepare_batch(batch):
    encoder_lengths = [len(entry[0]) for entry in batch]
    max_encoder_length = max(encoder_lengths)
    decoder_lengths = []
    max_decoder_length = max([len(entry[1]) for entry in batch])

    batch_encoder_inputs = []
    batch_decoder_inputs = []
    batch_targets = []
    batch_target_weights = []

    for source_seq, target_seq in batch:
        encoder_pads = (
            [seq2seq_util.PAD_ID] * (max_encoder_length - len(source_seq))
        )
        batch_encoder_inputs.append(
            list(reversed(source_seq)) + encoder_pads
        )

        decoder_pads = (
            [seq2seq_util.PAD_ID] * (max_decoder_length - len(target_seq))
        )
        target_seq_with_go_token = [seq2seq_util.GO_ID] + target_seq
        decoder_lengths.append(len(target_seq_with_go_token))
        batch_decoder_inputs.append(target_seq_with_go_token + decoder_pads)

        target_seq_with_eos = target_seq + [seq2seq_util.EOS_ID]
        targets = target_seq_with_eos + decoder_pads
        batch_targets.append(targets)

        if len(source_seq) + len(target_seq) == 0:
            target_weights = [0] * len(targets)
        else:
            target_weights = [
                1 if target != seq2seq_util.PAD_ID else 0
                for target in targets
            ]
        batch_target_weights.append(target_weights)

    return Batch(
        encoder_inputs=np.array(
            batch_encoder_inputs,
            dtype=np.int32,
        ).transpose(),
        encoder_lengths=np.array(encoder_lengths, dtype=np.int32),
        decoder_inputs=np.array(
            batch_decoder_inputs,
            dtype=np.int32,
        ).transpose(),
        decoder_lengths=np.array(decoder_lengths, dtype=np.int32),
        targets=np.array(
            batch_targets,
            dtype=np.int32,
        ).transpose(),
        target_weights=np.array(
            batch_target_weights,
            dtype=np.float32,
        ).transpose(),
    )
