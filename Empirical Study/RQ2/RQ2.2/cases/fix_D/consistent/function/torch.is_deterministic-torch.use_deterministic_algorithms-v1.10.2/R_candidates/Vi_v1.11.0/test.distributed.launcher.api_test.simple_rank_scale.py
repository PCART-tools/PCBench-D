def simple_rank_scale():
    rank = int(os.environ["RANK"])
    return 10 + rank
