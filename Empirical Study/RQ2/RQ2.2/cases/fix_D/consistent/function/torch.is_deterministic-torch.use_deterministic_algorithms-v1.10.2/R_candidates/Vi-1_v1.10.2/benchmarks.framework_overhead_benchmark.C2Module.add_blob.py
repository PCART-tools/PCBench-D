def add_blob(ws, blob_name, tensor_size):
    blob_tensor = np.random.randn(*tensor_size).astype(np.float32)
    ws.FeedBlob(blob_name, blob_tensor)
