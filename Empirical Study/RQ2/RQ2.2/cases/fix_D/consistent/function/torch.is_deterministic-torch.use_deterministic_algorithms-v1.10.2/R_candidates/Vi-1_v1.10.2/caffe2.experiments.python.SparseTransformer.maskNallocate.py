def maskNallocate(weight_name):
    """
    Combine mask and weights
    create wcsr, iw, jw, return their names
    """
    w = workspace.FetchBlob(weight_name)
    w_csr = scipy.sparse.csr_matrix(w)
    wcsr = w_csr.data
    iw = w_csr.indptr
    jw = w_csr.indices
    workspace.FeedBlob(weight_name + "wcsr", wcsr)
    workspace.FeedBlob(weight_name + "iw", iw)
    workspace.FeedBlob(weight_name + "jw", jw)
    return weight_name + "wcsr", weight_name + "iw", weight_name + "jw"
