def receive_and_send(queue, out_queue, event, count):
    for i in range(count):
        t = queue.get()
        out_queue.put(t.clone())
    event.wait()
