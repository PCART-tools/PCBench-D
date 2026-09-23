def randBlob(name, type, *dims, **kwargs):
    offset = kwargs['offset'] if 'offset' in kwargs else 0.0
    workspace.FeedBlob(name, np.random.rand(*dims).astype(type) + offset)
