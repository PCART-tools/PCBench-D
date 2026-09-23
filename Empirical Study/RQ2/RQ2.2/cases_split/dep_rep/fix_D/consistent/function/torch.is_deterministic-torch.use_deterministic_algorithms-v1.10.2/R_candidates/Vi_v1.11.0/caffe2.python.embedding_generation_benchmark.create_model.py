def create_model(args, queue, embedding_table, embedding_size):
    model = model_helper.ModelHelper(name='embedding_generation_bench')
    input_blob = model.net.DequeueBlobs(queue, 'input_data')

    if args.implementation == 'sinusoid':
        model.net.SinusoidPositionEncoding(
            [input_blob],
            ['output'],
            embedding_size=embedding_size
        )
    else:
        model.net.Gather(
            [embedding_table, input_blob],
            ['output'],
        )

    return model
