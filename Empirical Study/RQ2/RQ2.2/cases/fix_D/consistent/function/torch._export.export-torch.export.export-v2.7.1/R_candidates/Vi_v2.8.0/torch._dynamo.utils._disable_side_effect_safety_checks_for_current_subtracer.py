def _disable_side_effect_safety_checks_for_current_subtracer(fn, *args, **kwargs):
    return fn(*args, **kwargs)
