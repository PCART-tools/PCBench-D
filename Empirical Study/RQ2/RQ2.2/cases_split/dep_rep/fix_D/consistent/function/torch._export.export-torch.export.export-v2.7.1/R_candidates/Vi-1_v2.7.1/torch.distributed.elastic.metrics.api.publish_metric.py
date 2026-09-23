@deprecated(
    "Deprecated, use `put_metric(metric_group)(metric_name, metric_value)` instead",
    category=FutureWarning,
)
def publish_metric(metric_group: str, metric_name: str, metric_value: int):
    metric_stream = getStream(metric_group)
    metric_stream.add_value(metric_name, metric_value)
