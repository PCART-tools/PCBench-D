def send_and_delete_tensors(queue, event, device, dtype, count, size=5):
    for i in range(count):
        t = torch.full([size], i, device=device, dtype=dtype)
        queue.put(t)
        del t
    event.wait()
