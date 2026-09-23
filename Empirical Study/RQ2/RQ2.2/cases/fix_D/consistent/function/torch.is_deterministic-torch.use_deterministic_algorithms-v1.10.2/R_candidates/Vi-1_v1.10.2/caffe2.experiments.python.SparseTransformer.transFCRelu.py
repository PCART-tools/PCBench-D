def transFCRelu(cur, id2node, name2id, ops, model):
    """
    Add trans before and after this FC_Prune->(Relu)->FC_Prune chain.
    """
    # 1. add trans before the start of this chain
    # assuming that cur is a FC_Prune, and it has only one input
    pre = cur.prev.itervalues().next()
    # Create a node /op and insert it.
    # TODO(wyiming): check whether it is correct here
    current_blob = model.Transpose(cur.op.input[0], cur.op.input[0] + "_trans")
#     print model.net.Proto()
    trans_op = model.net.Proto().op[-1]
    trans_node = NetDefNode(trans_op.output[0], "Transpose", pre, trans_op)
    trans_node.visited = True
    pre_new = trans_node

    # 2. use while loop to visit the chain
    while True:
        # breakup with the parent
        cur.deleteInput(pre)
        if not (cur.optype == "FC_Prune" or cur.optype == "Relu"):
            print("Reaching the end of the chain")
            break
        if len(cur.ops) > 1:
            print("A FC/Relu giving more than 1 useful outputs")
        if cur.optype == "FC_Prune":
            op = cur.op
            wcsr, iw, jw = maskNallocate(op.input[1])
            bias_name = op.input[3]
            # TODO(wyiming): create a new Op here
            current_blob = model.FC_Sparse(current_blob,
                                           cur.op.output[0] + "_Sparse",
                                           wcsr, iw, jw, bias_name)
            sps_op = model.net.Proto().op[-1]
            sps_node = NetDefNode(cur.op.output[0] + "_Sparse",
                                  "FC_Sparse",
                                  pre_new, sps_op)
            sps_node.visited = True
            pre_new = sps_node
        if cur.optype == "Relu":
            op = cur.op
            current_blob = model.Relu(current_blob, current_blob)
            rel_op = model.net.Proto().op[-1]
            rel_node = NetDefNode(str(current_blob), "Relu",
                                  pre_new, rel_op)
            rel_node.visited = True
            pre_new = rel_node

        cur.visited = True
        pre = cur
        flag = False
        for _, temp in cur.ops.iteritems():
            if temp.optype == "Relu" or temp.optype == "FC_Prune":
                flag = True
                cur = temp
        if not flag:
            # assume that there is only 1 output that is not PrintOP
            cur = cur.ops.itervalues().next()
            cur.deleteInput(pre)
            print("No FC/RElu children")
            print(cur.op.type)
            break
    # 3. add trans after this chain like 1.
    current_blob = model.Transpose(current_blob, pre.op.output[0])
    trans_op = model.net.Proto().op[-1]
    trans_node = NetDefNode(str(current_blob), "Transpose", pre_new, trans_op)
    trans_node.visited = True
    cur.insertInput(trans_node)
    print(cur.prev)
    print(trans_node.ops)
