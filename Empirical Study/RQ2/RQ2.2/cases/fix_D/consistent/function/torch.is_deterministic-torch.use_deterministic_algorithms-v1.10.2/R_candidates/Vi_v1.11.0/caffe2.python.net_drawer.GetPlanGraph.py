def GetPlanGraph(plan_def, name=None, rankdir='TB'):
    graph = pydot.Dot(name, rankdir=rankdir)
    _draw_steps(plan_def.execution_step, graph)
    return graph
