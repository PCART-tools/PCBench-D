def build_embeddings(
    model,
    vocab_size,
    embedding_size,
    name,
    freeze_embeddings,
):
    embeddings = model.param_init_net.GaussianFill(
        [],
        name,
        shape=[vocab_size, embedding_size],
        std=0.1,
    )
    if not freeze_embeddings:
        model.params.append(embeddings)
    return embeddings
