def _determine_direction_for_categorical_split(fval: float, thresholds: str) -> str:
    if math.isnan(fval) or int(fval) < 0:
        return 'right'
    int_thresholds = {int(t) for t in thresholds.split('||')}
    return 'left' if int(fval) in int_thresholds else 'right'
