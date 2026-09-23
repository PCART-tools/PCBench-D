def _use_template_for_cpu(layout: Layout) -> bool:
    return use_max_autotune() and layout.device.type == "cpu"
