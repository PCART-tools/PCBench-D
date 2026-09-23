def _in_batch_shuffle_fn(data: DataChunk):
    random.shuffle(data)
    return data
