def num_ifs_loops(graph):
    graph_str = str(graph)
    # only look at body of graph
    graph_body = graph_str[0:graph_str.find("return")]
    return graph_body.count("prim::Loop") + graph_body.count("prim::If")
