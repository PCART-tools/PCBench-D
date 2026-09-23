def run_seq2seq_model(args, model_params=None):
    source_vocab = seq2seq_util.gen_vocab(
        args.source_corpus,
        args.unk_threshold,
    )
    target_vocab = seq2seq_util.gen_vocab(
        args.target_corpus,
        args.unk_threshold,
    )
    logger.info('Source vocab size {}'.format(len(source_vocab)))
    logger.info('Target vocab size {}'.format(len(target_vocab)))

    batches = gen_batches(args.source_corpus, args.target_corpus, source_vocab,
                          target_vocab, model_params['batch_size'],
                          args.max_length)
    logger.info('Number of training batches {}'.format(len(batches)))

    batches_eval = gen_batches(args.source_corpus_eval, args.target_corpus_eval,
                               source_vocab, target_vocab,
                               model_params['batch_size'], args.max_length)
    logger.info('Number of eval batches {}'.format(len(batches_eval)))

    with Seq2SeqModelCaffe2(
        model_params=model_params,
        source_vocab_size=len(source_vocab),
        target_vocab_size=len(target_vocab),
        num_gpus=args.num_gpus,
        num_cpus=20,
    ) as model_obj:
        model_obj.initialize_from_scratch()
        for i in range(args.epochs):
            logger.info('Epoch {}'.format(i))
            total_loss = 0
            for batch in batches:
                total_loss += model_obj.step(
                    batch=batch,
                    forward_only=False,
                )
            logger.info('\ttraining loss {}'.format(total_loss))
            total_loss = 0
            for batch in batches_eval:
                total_loss += model_obj.step(
                    batch=batch,
                    forward_only=True,
                )
            logger.info('\teval loss {}'.format(total_loss))
            if args.checkpoint is not None:
                model_obj.save(args.checkpoint, i)
