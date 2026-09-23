def generate_embedding_table(vocab_size, embedding_size):
    log.info("Generating embedding table with dimensions {}"
             .format([vocab_size, embedding_size]))

    generate_table_net = core.Net('generate_table')
    table = generate_table_net.GaussianFill(
        [],
        ['embedding_table'],
        shape=[vocab_size, embedding_size],
    )

    workspace.RunNetOnce(generate_table_net)
    return table
