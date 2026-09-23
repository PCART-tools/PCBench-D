def simple_fill(queue, event):
    data = queue.get()
    data[0][:] = 4
    event.set()
