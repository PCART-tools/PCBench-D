def random_topology_test(seed, *inp_tensor_list):
    np.random.seed(int(seed.numpy().tolist()))
    tensor_list = [*inp_tensor_list]
    num_tensor = len(tensor_list)

    # randomly add available constant value
    num_const = np.random.randint(0, num_tensor + 1)
    const_list = np.random.random(num_const)

    if DEBUG_PRINT:
        for const_item in const_list:
            print("----- real number {:.10f}", const_item)

    # we require all tensor to be in a single dependency set
    def get_root(x, dependency_map):
        if x in dependency_map:
            return get_root(dependency_map[x], dependency_map)
        else:
            return x
    d_map: Dict[int, int] = {}
    num_sets = num_tensor
    candidate = list(range(num_tensor))

    unary_operations = [torch.sigmoid, torch.relu]
    binary_operations = [torch.add, torch.sub, torch.mul]
    u_op_size = len(unary_operations)
    b_op_size = len(binary_operations)

    num_operations = np.random.randint(num_sets - 1,
                                       num_sets * GRAPH_FACTOR)

    ret_list = []

    while num_operations >= 0 or num_sets > 1:
        # we start off with randomly pick a candidate and operation
        index = np.random.randint(0, len(candidate))
        op_index = np.random.randint(0, u_op_size + b_op_size)
        lh_index = candidate[index]
        rh_index = None
        out_tensor = None

        if DEBUG_PRINT:
            print("iteration {0}, num_sets{1}, candidates {2}, tensor_list {3}, lh_index {4}, op_index {5}".format(
                num_operations, num_sets, candidate, len(tensor_list), lh_index, op_index))
        if num_operations >= 0:
            num_operations -= 1
            if op_index < u_op_size:
                # unary operation, we just apply a random operation on candidate
                out_tensor = unary_operations[op_index](tensor_list[lh_index])
            else:
                # binary operation, we randomly choose the other operand:
                #   1. tensor on tensor operation -> rh_index
                #   2. tensor on const operation
                # we are not restricted to candidate tensor any more.
                op_2_index = np.random.randint(0, len(tensor_list) + num_const)

                if op_2_index < len(tensor_list):
                    if op_2_index == lh_index:
                        # if we are unlucky that we picked on the candidate again, just try
                        # another tensor
                        op_2_index = (op_2_index + 1) % len(tensor_list)
                    # [if rh_index: create binary operator output tensor]
                    rh_index = op_2_index
                else:
                    left = tensor_list[lh_index]
                    right = const_list[op_2_index - len(tensor_list)]
                    # if np.random.randint(0, 2) > 0:
                    #  left = const_list[op_2_index - len(tensor_list)]
                    #  right = tensor_list[lh_index]
                    out_tensor = binary_operations[op_index - u_op_size](left, right)
                if DEBUG_PRINT:
                    print("binary, op_2_index {0}, rh_index ?{1}".format(op_2_index, rh_index))
        else:
            # binary operation, we just randomly pick two candidates.
            # this is not the most efficient way to close dependecy, as we could have
            # two candidate that are actually connected
            cand_index = np.random.randint(0, len(candidate))
            if cand_index == index:
                cand_index = (cand_index + 1) % len(candidate)
            # [if rh_index: create binary operator output tensor]
            rh_index = candidate[cand_index]
            if DEBUG_PRINT:
                print("binary rh_index ?{0}".format(rh_index))

        # update candidate should happen before we remove rh_index
        candidate[index] = len(tensor_list)
        lh_root = get_root(lh_index, d_map)
        # [if rh_index: create binary operator output tensor]
        if rh_index is not None:

            out_tensor = binary_operations[op_index - u_op_size](
                tensor_list[lh_index],
                tensor_list[rh_index])

            # remove rh_index from candidate if it is used
            if rh_index in candidate:
                # python remove(val), not by index
                candidate.remove(rh_index)

            # check if we join dependency sets:
            rh_root = get_root(rh_index, d_map)
            if lh_root != rh_root:
                num_sets -= 1
                # update dependency, no need to update d_map[rh_root] when
                # they are already pointing the same root
                d_map[rh_root] = len(tensor_list)

        # no joining, just update dependency
        d_map[lh_root] = len(tensor_list)

        # update candidate, this avoids us applying identical operation on
        # the same tensor(s)
        tensor_list.append(out_tensor)

    # TODO: we should mark
    #       union(random_sample(tensor_list[num_tensor:]), candidate) as outputs.
    #       which would ensure we have no dead branch and a connected computation
    #       graph. However, it won't work easily if we have broadcast.
    # I have disabled broadcast for now to focus on topology test.
    for ind in candidate:
        ret_list.append(tensor_list[ind])

    out_list = np.random.choice(
        range(num_tensor, len(tensor_list)),
        np.random.randint(0, len(tensor_list) - num_tensor),
        False)
    for ind in out_list:
        if ind not in candidate:
            ret_list.append(tensor_list[ind])

    if DEBUG_PRINT:
        print("ended with tensor_list: {0}".format(len(tensor_list)))

    return tuple(ret_list)
