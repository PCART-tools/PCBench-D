@Printer.register(OperatorDef)
def print_op(text, op):
    args = [(a.name, _arg_val(a)) for a in op.arg]
    dev_opt_txt = format_device_option(op.device_option)
    if dev_opt_txt:
        args.append(('device_option', dev_opt_txt))

    if text.c2_net_name:
        text.add(call(
            text.c2_net_name + '.' + op.type,
            [list(op.input), list(op.output)] + args))
    else:
        text.add(call(
            op.type,
            list(op.input) + args,
            op.output,
            factor_prefixes=text.factor_prefixes))
    for arg in op.arg:
        if arg.HasField('n'):
            with text.context('arg: %s' % arg.name):
                text(arg.n)
