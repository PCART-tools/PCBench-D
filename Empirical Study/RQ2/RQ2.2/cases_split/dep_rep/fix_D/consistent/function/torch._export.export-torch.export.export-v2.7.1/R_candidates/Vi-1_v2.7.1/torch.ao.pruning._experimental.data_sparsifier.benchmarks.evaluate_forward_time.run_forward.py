def run_forward(model, **batch):
    """The purpose of this function is to time the forward run of the model.
    The model forward happens a 100 times and each pass is timed. The average
    of this 100 runs is returned as avg_time.
    """
    time_list = []
    X, lS_o, lS_i = batch["X"], batch["lS_o"], batch["lS_i"]
    for _ in range(100):
        start = time.time()
        with torch.no_grad():
            model(X, lS_o, lS_i)
        end = time.time()
        time_taken = end - start
        time_list.append(time_taken)
    avg_time = np.mean(time_list[1:])
    return avg_time
