def GetOperatorMapForPlan(plan_def):
    operator_map = {}
    for net_id, net in enumerate(plan_def.network):
        if net.HasField('name'):
            operator_map[plan_def.name + "_" + net.name] = net.op
        else:
            operator_map[plan_def.name + "_network_%d" % net_id] = net.op
    return operator_map
