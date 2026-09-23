def _has_same_attr(
    qspec_a: QuantizationSpecBase, qspec_b: QuantizationSpecBase, attr_name: str
):
    return (
        hasattr(qspec_a, attr_name)
        and hasattr(qspec_b, attr_name)
        and getattr(qspec_a, attr_name) == getattr(qspec_b, attr_name)
    ) or (not hasattr(qspec_a, attr_name) and not hasattr(qspec_b, attr_name))
