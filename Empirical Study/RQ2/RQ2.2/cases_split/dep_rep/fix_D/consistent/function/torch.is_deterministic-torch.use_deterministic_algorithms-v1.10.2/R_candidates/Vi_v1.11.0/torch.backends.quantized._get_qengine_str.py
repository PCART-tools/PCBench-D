def _get_qengine_str(qengine: int) -> str:
    all_engines = {0 : 'none', 1 : 'fbgemm', 2 : 'qnnpack'}
    return all_engines.get(qengine, '*undefined')
