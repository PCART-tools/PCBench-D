def requires_grad_variable_sharing(queue, ready):
    var = queue.get()
    ready.set()
    queue.put(var.requires_grad)
