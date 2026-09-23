def video_input(model, blob_in, blob_out, **kwargs):
    # size of outputs can vary depending on kwargs
    outputs = model.net.VideoInput(blob_in, blob_out, **kwargs)
    return outputs
