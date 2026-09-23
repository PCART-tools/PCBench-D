def _parse_gufunc_signature(signature):
    """
    Parse string signatures for a generalized universal function.

    Arguments
    ---------
    signature : string
        Generalized universal function signature, e.g., ``(m,n),(n,p)->(m,p)``
        for ``np.matmul``.

    Returns
    -------
    Tuple of input and output core dimensions parsed from the signature, each
    of the form List[Tuple[str, ...]], except for one output. For one  output
    core dimension is not a list, but of the form Tuple[str, ...]
    """
    signature = signature.replace(' ', '')
    if not re.match(_SIGNATURE, signature):
        raise ValueError('Not a valid gufunc signature: {}'.format(signature))
    in_txt, out_txt = signature.split('->')
    ins = [tuple(re.findall(_DIMENSION_NAME, arg))
           for arg in re.findall(_ARGUMENT, in_txt)]
    outs = [tuple(re.findall(_DIMENSION_NAME, arg))
            for arg in re.findall(_ARGUMENT, out_txt)]
    outs = outs[0] if ((len(outs) == 1) and (out_txt[-1] != ',')) else outs
    return ins, outs
