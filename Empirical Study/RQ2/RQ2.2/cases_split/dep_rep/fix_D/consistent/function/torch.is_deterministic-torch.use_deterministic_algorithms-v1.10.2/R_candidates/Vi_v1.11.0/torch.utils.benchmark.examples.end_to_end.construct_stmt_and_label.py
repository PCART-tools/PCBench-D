def construct_stmt_and_label(pr, params):
    if pr == "39850":
        k0, k1, k2, dim = [params[i] for i in ["k0", "k1", "k2", "dim"]]
        state = np.random.RandomState(params["random_value"])
        topk_dim = state.randint(low=0, high=dim)
        dim_size = [k0, k1, k2][topk_dim]
        k = max(int(np.floor(2 ** state.uniform(low=0, high=np.log2(dim_size)))), 1)

        return f"torch.topk(x, dim={topk_dim}, k={k})", "topk"

    if pr == "39967":
        return "torch.std(x)", "std"

    if pr == "39744":
        state = np.random.RandomState(params["random_value"])
        sort_dim = state.randint(low=0, high=params["dim"])
        return f"torch.sort(x, dim={sort_dim})", "sort"

    raise ValueError("Unknown PR")
