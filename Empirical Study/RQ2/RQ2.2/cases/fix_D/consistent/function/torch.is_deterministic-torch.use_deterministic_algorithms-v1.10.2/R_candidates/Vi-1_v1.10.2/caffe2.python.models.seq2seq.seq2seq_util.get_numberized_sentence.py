def get_numberized_sentence(sentence, vocab):
    numerized_sentence = []
    for token in sentence.strip().split():
        if token in vocab:
            numerized_sentence.append(vocab[token])
        else:
            numerized_sentence.append(vocab[UNK])
    return numerized_sentence
