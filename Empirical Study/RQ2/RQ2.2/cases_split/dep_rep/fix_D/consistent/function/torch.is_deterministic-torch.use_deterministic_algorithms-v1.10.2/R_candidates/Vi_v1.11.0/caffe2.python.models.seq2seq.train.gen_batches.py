def gen_batches(source_corpus, target_corpus, source_vocab, target_vocab,
                batch_size, max_length):
    with open(source_corpus) as source, open(target_corpus) as target:
        parallel_sentences = []
        for source_sentence, target_sentence in zip(source, target):
            numerized_source_sentence = seq2seq_util.get_numberized_sentence(
                source_sentence,
                source_vocab,
            )
            numerized_target_sentence = seq2seq_util.get_numberized_sentence(
                target_sentence,
                target_vocab,
            )
            if (
                len(numerized_source_sentence) > 0 and
                len(numerized_target_sentence) > 0 and
                (
                    max_length is None or (
                        len(numerized_source_sentence) <= max_length and
                        len(numerized_target_sentence) <= max_length
                    )
                )
            ):
                parallel_sentences.append((
                    numerized_source_sentence,
                    numerized_target_sentence,
                ))
    parallel_sentences.sort(key=lambda s_t: (len(s_t[0]), len(s_t[1])))

    batches, batch = [], []
    for sentence_pair in parallel_sentences:
        batch.append(sentence_pair)
        if len(batch) >= batch_size:
            batches.append(batch)
            batch = []
    if len(batch) > 0:
        while len(batch) < batch_size:
            batch.append(batch[-1])
        assert len(batch) == batch_size
        batches.append(batch)
    random.shuffle(batches)
    return batches
