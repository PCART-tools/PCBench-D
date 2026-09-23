def _test_cuda_ipc_deadlock_learner(queue, iterations):
    net = torch.nn.LSTM(1, 1).cuda()
    for i in range(iterations):
        if not queue.full():
            queue.put(copy.deepcopy(net.state_dict()))
        time.sleep(.01)
