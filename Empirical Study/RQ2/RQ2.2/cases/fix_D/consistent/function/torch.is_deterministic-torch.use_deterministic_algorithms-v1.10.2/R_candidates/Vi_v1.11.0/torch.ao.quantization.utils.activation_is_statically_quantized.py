def activation_is_statically_quantized(qconfig):
    """ Given a qconfig, decide if the activation needs to be
    quantized or not, this includes quantizing to quint8, qint8 and float16
    """
    return activation_dtype(qconfig) in [torch.quint8, torch.qint8, torch.float16]
