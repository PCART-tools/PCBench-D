def to_html(nodes):
    listeners = []
    for i, n in enumerate(nodes):
        if n.context is None:
            continue
        s = _listener_template.format(id=str(i + 1), stack=escape(f'{n.label}:\n{n.context}'))
        listeners.append(s)
    dot = to_dot(nodes)
    return _template.replace('$DOT', repr(dot)).replace('$LISTENERS', '\n'.join(listeners))
