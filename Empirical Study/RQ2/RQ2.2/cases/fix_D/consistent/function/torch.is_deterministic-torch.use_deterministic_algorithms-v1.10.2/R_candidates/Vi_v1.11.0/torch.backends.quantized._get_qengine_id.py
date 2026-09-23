def _get_qengine_id(qengine: str) -> int:
    if qengine == 'none' or qengine == '' or qengine is None:
        ret = 0
    elif qengine == 'fbgemm':
        ret = 1
    elif qengine == 'qnnpack':
        ret = 2
    else:
        ret = -1
        raise RuntimeError("{} is not a valid value for quantized engine".format(qengine))
    return ret
