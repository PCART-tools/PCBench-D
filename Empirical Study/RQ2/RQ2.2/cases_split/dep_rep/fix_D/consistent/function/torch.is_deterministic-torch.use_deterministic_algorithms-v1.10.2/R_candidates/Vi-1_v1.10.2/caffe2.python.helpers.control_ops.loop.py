def loop(model, cond_blob, external_blobs, loop_model, cond_model=None):
    """Loop"""
    add_while_op(
        model.net,
        cond_blob,
        external_blobs,
        loop_model.net,
        cond_model.net if cond_model else None)
