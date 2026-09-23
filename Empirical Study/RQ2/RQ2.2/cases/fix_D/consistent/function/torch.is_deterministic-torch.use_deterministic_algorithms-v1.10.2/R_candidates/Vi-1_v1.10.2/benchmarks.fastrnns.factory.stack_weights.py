def stack_weights(weights):
    def unzip_columns(mat):
        assert isinstance(mat, list)
        assert isinstance(mat[0], list)
        layers = len(mat)
        columns = len(mat[0])
        return [[mat[layer][col] for layer in range(layers)]
                for col in range(columns)]

    # XXX: script fns have problems indexing multidim lists, so we try to
    # avoid them by stacking tensors
    all_weights = weights
    packed_weights = [torch.stack(param)
                      for param in unzip_columns(all_weights)]
    return packed_weights
