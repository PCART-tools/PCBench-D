def configure(handler: MetricHandler, group: Optional[str] = None):
    if group is None:
        global _default_metrics_handler
        # pyre-fixme[9]: _default_metrics_handler has type `NullMetricHandler`; used
        #  as `MetricHandler`.
        _default_metrics_handler = handler
    else:
        _metrics_map[group] = handler
