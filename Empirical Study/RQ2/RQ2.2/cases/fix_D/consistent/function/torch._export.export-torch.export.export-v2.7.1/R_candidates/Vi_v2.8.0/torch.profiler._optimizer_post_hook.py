def _optimizer_post_hook(optimizer, args, kwargs):
    KinetoStepTracker.increment_step("Optimizer")
