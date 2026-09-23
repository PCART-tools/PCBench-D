def call(op, inputs=None, outputs=None, factor_prefixes=False):
    if not inputs:
        inputs = ''
    else:
        inputs_v = [a for a in inputs if not isinstance(a, tuple)]
        inputs_kv = [a for a in inputs if isinstance(a, tuple)]
        inputs = ', '.join(
            x
            for x in chain(
                [factor_prefix(inputs_v, factor_prefixes)],
                ('%s=%s' % kv for kv in inputs_kv),
            )
            if x
        )
    call = '%s(%s)' % (op, inputs)
    return call if not outputs else '%s = %s' % (
        factor_prefix(outputs, factor_prefixes), call)
