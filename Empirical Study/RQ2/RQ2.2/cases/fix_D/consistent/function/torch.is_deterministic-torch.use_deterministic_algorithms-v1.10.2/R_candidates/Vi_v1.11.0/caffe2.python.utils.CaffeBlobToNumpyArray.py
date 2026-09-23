def CaffeBlobToNumpyArray(blob):
    if (blob.num != 0):
        # old style caffe blob.
        return (np.asarray(blob.data, dtype=np.float32)
                .reshape(blob.num, blob.channels, blob.height, blob.width))
    else:
        # new style caffe blob.
        return (np.asarray(blob.data, dtype=np.float32)
                .reshape(blob.shape.dim))
