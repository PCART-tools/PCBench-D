def _draw_steps(steps, g, skip_step_edges=False):  # noqa
    kMaxParallelSteps = 3

    def get_label():
        label = [step.name + '\n']
        if step.report_net:
            label.append('Reporter: {}'.format(step.report_net))
        if step.should_stop_blob:
            label.append('Stopper: {}'.format(step.should_stop_blob))
        if step.concurrent_substeps:
            label.append('Concurrent')
        if step.only_once:
            label.append('Once')
        return '\n'.join(label)

    def substep_edge(start, end):
        return pydot.Edge(start, end, arrowhead='dot', style='dashed')

    nodes = []
    for i, step in enumerate(steps):
        parallel = step.concurrent_substeps

        nodes.append(pydot.Node(_escape_label(get_label()), **OP_STYLE))
        g.add_node(nodes[-1])

        if i > 0 and not skip_step_edges:
            g.add_edge(pydot.Edge(nodes[-2], nodes[-1]))

        if step.network:
            sub_nodes = _draw_nets(step.network, g)
        elif step.substep:
            if parallel:
                sub_nodes = _draw_steps(
                    step.substep[:kMaxParallelSteps], g, skip_step_edges=True)
            else:
                sub_nodes = _draw_steps(step.substep, g)
        else:
            raise ValueError('invalid step')

        if parallel:
            for sn in sub_nodes:
                g.add_edge(substep_edge(nodes[-1], sn))
            if len(step.substep) > kMaxParallelSteps:
                ellipsis = pydot.Node('{} more steps'.format(
                    len(step.substep) - kMaxParallelSteps), **OP_STYLE)
                g.add_node(ellipsis)
                g.add_edge(substep_edge(nodes[-1], ellipsis))
        else:
            g.add_edge(substep_edge(nodes[-1], sub_nodes[0]))

    return nodes
