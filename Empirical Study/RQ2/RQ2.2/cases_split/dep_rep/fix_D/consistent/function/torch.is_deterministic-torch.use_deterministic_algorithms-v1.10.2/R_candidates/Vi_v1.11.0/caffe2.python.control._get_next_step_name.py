def _get_next_step_name(control_name, base_name):
    global _current_idx, _used_step_names
    concat_name = '%s/%s' % (base_name, control_name)
    next_name = concat_name
    while next_name in _used_step_names:
        next_name = '%s_%d' % (concat_name, _current_idx)
        _current_idx += 1
    _used_step_names.add(next_name)
    return next_name
