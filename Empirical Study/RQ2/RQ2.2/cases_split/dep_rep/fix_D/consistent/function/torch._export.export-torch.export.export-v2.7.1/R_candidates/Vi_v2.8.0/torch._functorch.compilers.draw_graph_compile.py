def draw_graph_compile(name):
    return make_boxed_compiler(partial(_draw_graph_compile, name=name))
