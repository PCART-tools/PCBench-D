@map_impl.py_autograd_impl
def map_autograd(f, xs, pos_args):
    num_mapped_args = len(xs)
    fw_graph, bw_graph = create_fw_bw_graph(f, num_mapped_args, *xs, *pos_args)
    flat_out = MapAutogradOp.apply(fw_graph, bw_graph, num_mapped_args, *xs, *pos_args)
    return flat_out
