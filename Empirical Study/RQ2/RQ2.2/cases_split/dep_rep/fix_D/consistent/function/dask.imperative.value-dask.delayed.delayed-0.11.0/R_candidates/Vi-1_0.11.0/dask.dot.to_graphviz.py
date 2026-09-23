def to_graphviz(dsk, data_attributes=None, function_attributes=None, **kwargs):
    if data_attributes is None:
        data_attributes = {}
    if function_attributes is None:
        function_attributes = {}

    attributes = {'rankdir': 'BT'}
    attributes.update(kwargs)
    g = graphviz.Digraph(graph_attr=attributes)

    seen = set()
    cache = {}

    for k, v in dsk.items():
        k_name = name(k)
        if k_name not in seen:
            seen.add(k_name)
            g.node(k_name, label=label(k, cache=cache), shape='box',
                   **data_attributes.get(k, {}))

        if istask(v):
            func_name = name((k, 'function'))
            if func_name not in seen:
                seen.add(func_name)
                g.node(func_name, label=task_label(v), shape='circle',
                       **function_attributes.get(k, {}))
            g.edge(func_name, k_name)

            for dep in get_dependencies(dsk, k):
                dep_name = name(dep)
                if dep_name not in seen:
                    seen.add(dep_name)
                    g.node(dep_name, label=label(dep, cache=cache), shape='box',
                           **data_attributes.get(dep, {}))
                g.edge(dep_name, func_name)
        elif ishashable(v) and v in dsk:
            g.edge(name(v), k_name)
    return g
