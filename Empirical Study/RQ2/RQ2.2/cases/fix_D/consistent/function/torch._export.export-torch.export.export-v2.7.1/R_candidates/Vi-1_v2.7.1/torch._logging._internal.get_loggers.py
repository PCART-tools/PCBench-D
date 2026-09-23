def get_loggers():
    """
    Returns: a list of all registered loggers
    """
    return [logging.getLogger(qname) for qname in log_registry.get_log_qnames()]
