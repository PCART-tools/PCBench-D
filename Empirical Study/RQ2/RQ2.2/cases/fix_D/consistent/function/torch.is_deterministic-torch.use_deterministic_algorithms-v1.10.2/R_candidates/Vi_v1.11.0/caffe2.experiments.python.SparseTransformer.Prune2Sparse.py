def Prune2Sparse(cur, id2node, name2id, ops, model):
    # Assume that FC and Relu takes in only 1 input;
    # If not raise warning
    if not cur.visited and cur.optype == "FC_Prune":
        transFCRelu(cur, id2node, name2id, ops, model)

    cur.visited = True
    for name, n in cur.ops.iteritems():
        Prune2Sparse(n, id2node, name2id, ops, model)
