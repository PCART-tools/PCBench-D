def dequeue_value(queue):
    dequeue_blob = 'dequeue_blob'
    workspace.RunOperatorOnce(
        core.CreateOperator(
            "SafeDequeueBlobs", [queue], [dequeue_blob, 'status_blob']
        )
    )

    return workspace.FetchBlob(dequeue_blob)
