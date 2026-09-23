def sum_tensors(inq, outq):
    with torch.cuda.device(1):
        tensors = inq.get()
        for tensor in tensors:
            outq.put((tensor.sum().item(), tensor.get_device(),
                      tensor.numel(), tensor.storage().size()))
