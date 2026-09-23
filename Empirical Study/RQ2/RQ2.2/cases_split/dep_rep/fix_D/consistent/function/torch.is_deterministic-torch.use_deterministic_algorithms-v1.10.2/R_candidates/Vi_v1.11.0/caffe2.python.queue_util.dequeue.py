def dequeue(net, queue, num_blobs, status=None, field_names=None,
            num_records=1):
    if field_names is not None:
        assert len(field_names) == num_blobs
        data_names = [net.NextName(name) for name in field_names]
    else:
        data_names = [net.NextName('data', i) for i in range(num_blobs)]
    if status is None:
        status = net.NextName('status')
    results = net.SafeDequeueBlobs(
        queue, data_names + [status], num_records=num_records)
    results = list(results)
    status_blob = results.pop(-1)
    return results, status_blob
