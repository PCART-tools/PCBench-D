def _dist_sum(wait=0):
    rank = int(os.environ["RANK"])
    dist.init_process_group(backend="gloo")
    t = torch.tensor(rank)

    time.sleep(wait)
    dist.all_reduce(t, op=dist.reduce_op.SUM)
    return t.item()
