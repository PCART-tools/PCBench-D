def receive_and_send_sum(queue, out_queue, event, device, dtype, count, size=5):
    s = torch.full([size], 0, device=device, dtype=dtype)
    for i in range(count):
        t = queue.get()
        s += t
    out_queue.put(s)
    event.wait()
