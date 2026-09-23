def _test_cuda_ipc_deadlock_actor(queue, iterations):
    for i in range(iterations):
        if not queue.empty():
            queue.get()
        time.sleep(.01)
