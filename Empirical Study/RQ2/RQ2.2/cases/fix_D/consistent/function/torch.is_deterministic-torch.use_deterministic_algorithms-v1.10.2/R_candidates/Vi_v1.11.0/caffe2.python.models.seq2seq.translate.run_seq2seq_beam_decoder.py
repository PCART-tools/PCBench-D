def run_seq2seq_beam_decoder(args, model_params, decoding_params):
    source_vocab = seq2seq_util.gen_vocab(
        args.source_corpus,
        args.unk_threshold,
    )
    logger.info('Source vocab size {}'.format(len(source_vocab)))
    target_vocab = seq2seq_util.gen_vocab(
        args.target_corpus,
        args.unk_threshold,
    )
    inversed_target_vocab = {v: k for (k, v) in viewitems(target_vocab)}
    logger.info('Target vocab size {}'.format(len(target_vocab)))

    decoder = Seq2SeqModelCaffe2EnsembleDecoder(
        translate_params=dict(
            ensemble_models=[dict(
                source_vocab=source_vocab,
                target_vocab=target_vocab,
                model_params=model_params,
                model_file=args.checkpoint,
            )],
            decoding_params=decoding_params,
        ),
    )
    decoder.load_models()

    for line in sys.stdin:
        numerized_source_sentence = seq2seq_util.get_numberized_sentence(
            line,
            source_vocab,
        )
        translation, alignment, _ = decoder.decode(
            numerized_source_sentence,
            2 * len(numerized_source_sentence) + 5,
        )
        print(' '.join([inversed_target_vocab[tid] for tid in translation]))
