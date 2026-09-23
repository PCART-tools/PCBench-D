def fc_sparse(
    model, blob_in, blob_out, w_csr, iw, jw, bias,
    **kwargs
):
    """FC_Sparse: Only takes in allocated weights"""
    if not (w_csr and iw and jw and bias):
        print("Warning...")
    model.AddParameter(w_csr)
    model.AddParameter(iw)
    model.AddParameter(jw)
    model.AddParameter(bias)
    return model.net.FC_Sparse([blob_in, w_csr, iw, jw, bias],
                               blob_out, **kwargs)
