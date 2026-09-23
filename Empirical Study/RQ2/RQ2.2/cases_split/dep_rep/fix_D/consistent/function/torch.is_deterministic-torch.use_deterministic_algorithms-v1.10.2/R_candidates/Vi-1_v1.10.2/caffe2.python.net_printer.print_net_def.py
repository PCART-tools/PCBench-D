@Printer.register(NetDef)
def print_net_def(text, net_def):
    if text.c2_syntax:
        text.add(call('core.Net', ["'%s'" % net_def.name], [net_def.name]))
        text.c2_net_name = net_def.name
    else:
        text.add('# net: %s' % net_def.name)
    for op in net_def.op:
        text(op)
    if text.c2_syntax:
        text.c2_net_name = None
