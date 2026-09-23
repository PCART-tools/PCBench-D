def generate_fx_example():
    name = 'simple_leaf'
    model = SimpleWithLeaf(5, 10)
    graph_module : torch.fx.GraphModule = symbolic_trace(model)
    with PackageExporter(str(p / (name + "_fx"))) as e:
        e.intern("**")
        e.save_pickle("model", "model.pkl", graph_module)

    model_jit = torch.jit.script(model)
    model_jit.save(str(p / (name + "_jit")))
