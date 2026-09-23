def CallWithExceptionIntercept(func, op_id_fetcher, net_name, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception:
        op_id = op_id_fetcher()
        net_tracebacks = operator_tracebacks.get(net_name, None)
        logger.warning(
            'Original python traceback for operator `{}` in network '
            '`{}` in exception above (most recent call last):'.format(
                op_id, net_name))
        if net_tracebacks and op_id in net_tracebacks:
            tb = net_tracebacks[op_id]
            for line in reversed(tb):
                logger.warning('  File "{}", line {}, in {}'.format(
                    line[0], line[1], line[2]))
        raise
