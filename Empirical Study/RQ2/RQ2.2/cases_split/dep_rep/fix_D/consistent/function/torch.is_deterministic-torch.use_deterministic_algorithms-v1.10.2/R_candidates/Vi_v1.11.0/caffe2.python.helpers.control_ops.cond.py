def cond(model, cond_blob, external_blobs, then_model, else_model=None):
    """Condition"""
    add_if_op(
        model.net,
        cond_blob,
        external_blobs,
        then_model.net,
        else_model.net if else_model else None)
