def _refresh_per_optimizer_state():
    return {"stage": OptState.READY, "found_inf_per_device": {}}
