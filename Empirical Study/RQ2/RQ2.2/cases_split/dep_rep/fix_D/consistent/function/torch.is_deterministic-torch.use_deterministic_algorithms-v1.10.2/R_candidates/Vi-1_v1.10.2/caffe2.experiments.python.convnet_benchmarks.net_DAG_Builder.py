def net_DAG_Builder(model):
    print("====================================================")
    print("                 Start Building DAG                 ")
    print("====================================================")
    net_root = SparseTransformer.netbuilder(model)
    return net_root
