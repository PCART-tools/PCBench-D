def gen_vocab(corpus, unk_threshold):
    vocab = collections.defaultdict(lambda: len(vocab))
    freqs = collections.defaultdict(lambda: 0)
    # Adding padding tokens to the vocabulary to maintain consistency with IDs
    vocab[PAD]
    vocab[GO]
    vocab[EOS]
    vocab[UNK]

    with open(corpus) as f:
        for sentence in f:
            tokens = sentence.strip().split()
            for token in tokens:
                freqs[token] += 1
    for token, freq in viewitems(freqs):
        if freq > unk_threshold:
            vocab[token]

    return vocab
