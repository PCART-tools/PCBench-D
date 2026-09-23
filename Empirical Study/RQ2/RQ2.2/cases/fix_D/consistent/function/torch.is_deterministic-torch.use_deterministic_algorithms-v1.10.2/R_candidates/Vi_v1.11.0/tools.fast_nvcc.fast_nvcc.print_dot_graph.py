def print_dot_graph(
    *,
    commands: List[List[str]],
    graph: Graph,
    filename: str,
) -> None:
    """
    Print a DOT file displaying short versions of the commands in graph.
    """
    def name(k: int) -> str:
        return f'"{k} {os.path.basename(commands[k][0])}"'
    with open(filename, 'w') as f:
        print('digraph {', file=f)
        # print all nodes, in case it's disconnected
        for i in range(len(graph)):
            print(f'    {name(i)};', file=f)
        for i, deps in enumerate(graph):
            for j in deps:
                print(f'    {name(j)} -> {name(i)};', file=f)
        print('}', file=f)
