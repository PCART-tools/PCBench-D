def release_blobs_when_used(netproto, dont_free_blobs, selector_fun=None):
    '''
    Insert Free-ops after a blob has been used the last time, so that its
    memory can be reclaimed. Use this only with efficient caching memory
    managers (such as CUB, --caffe2_cuda_memory_pool=cub).

    Blobs used with Alias op won't be freed.

    @dont_free_blobs:  is a set of blobs that should not be freed
    @selector_fun:     optional lambda that return True if blob name
                       can be released. Use for easy special filtering, like
                       excluding blobs with "loss" in the name.

    Returns a new protobuffer. To use with a model, use:
        model.net._net = memonger.release_blobs_when_used(..)
    '''
    input_blobs = set()
    can_release = set()
    alias_blobs = set()
    netproto = copy.deepcopy(netproto)

    for op in netproto.op:
        if op.type == 'Alias':
            alias_blobs.add(op.input[0])
            continue
        for inp in op.input:
            input_blobs.add(inp)
        for outp in op.output:
            if outp not in input_blobs:
                if selector_fun is None or selector_fun(outp):
                    can_release.add(outp)

    # Remove such blobs that are not input at all and external outputs
    can_release = can_release - set(netproto.external_output)
    can_release = can_release.intersection(input_blobs)
    can_release = can_release - dont_free_blobs
    can_release = can_release - alias_blobs

    ops = list(netproto.op)

    # .. then find last use of each can-release blob, and insert a Free op
    for j in reversed(range(0, len(netproto.op))):
        op = netproto.op[j]
        for inp in op.input:
            if inp in can_release:
                can_release.remove(inp)
                ops.insert(j + 1, core.CreateOperator("Free", [inp], [inp]))

    del netproto.op[:]
    netproto.op.extend(ops)
    return netproto
