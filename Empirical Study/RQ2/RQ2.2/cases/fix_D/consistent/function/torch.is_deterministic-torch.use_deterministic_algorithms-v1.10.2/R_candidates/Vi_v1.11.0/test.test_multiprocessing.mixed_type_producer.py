def mixed_type_producer(queue, event):
    for _ in range(10):
        float_tensor = torch.ones(2, 2).float().cuda()
        byte_tensor = torch.zeros(2, 2).byte().cuda()

        queue.put(float_tensor)
        queue.put(byte_tensor)
        event.wait()
        event.clear()
