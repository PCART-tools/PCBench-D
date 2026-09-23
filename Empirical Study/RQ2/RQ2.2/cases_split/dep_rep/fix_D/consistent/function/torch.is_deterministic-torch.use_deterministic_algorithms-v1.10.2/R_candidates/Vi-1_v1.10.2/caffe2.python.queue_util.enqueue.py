def enqueue(net, queue, data_blobs, status=None):
    if status is None:
        status = net.NextName('status')
    # Enqueueing moved the data into the queue;
    # duplication will result in data corruption
    queue_blobs = []
    for blob in data_blobs:
        if blob not in queue_blobs:
            queue_blobs.append(blob)
        else:
            logger.warning("Need to copy blob {} to enqueue".format(blob))
            queue_blobs.append(net.Copy(blob))
    results = net.SafeEnqueueBlobs([queue] + queue_blobs, queue_blobs + [status])
    return results[-1]
