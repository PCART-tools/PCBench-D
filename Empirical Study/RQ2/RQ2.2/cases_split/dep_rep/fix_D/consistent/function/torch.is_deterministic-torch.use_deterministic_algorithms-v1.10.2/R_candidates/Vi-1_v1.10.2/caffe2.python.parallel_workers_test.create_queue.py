def create_queue():
    queue = 'queue'

    workspace.RunOperatorOnce(
        core.CreateOperator(
            "CreateBlobsQueue", [], [queue], num_blobs=1, capacity=1000
        )
    )
    # Technically, blob creations aren't thread safe. Since the unittest below
    # does RunOperatorOnce instead of CreateNet+RunNet, we have to precreate
    # all blobs beforehand
    for i in range(100):
        workspace.C.Workspace.current.create_blob("blob_" + str(i))
        workspace.C.Workspace.current.create_blob("status_blob_" + str(i))
    workspace.C.Workspace.current.create_blob("dequeue_blob")
    workspace.C.Workspace.current.create_blob("status_blob")

    return queue
