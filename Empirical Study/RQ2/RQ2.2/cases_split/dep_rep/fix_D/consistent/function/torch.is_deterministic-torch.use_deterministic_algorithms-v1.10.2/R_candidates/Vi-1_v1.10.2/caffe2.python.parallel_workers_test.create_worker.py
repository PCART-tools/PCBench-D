def create_worker(queue, get_blob_data):
    def dummy_worker(worker_id):
        blob = 'blob_' + str(worker_id)

        workspace.FeedBlob(blob, get_blob_data(worker_id))

        workspace.RunOperatorOnce(
            core.CreateOperator(
                'SafeEnqueueBlobs', [queue, blob], [blob, 'status_blob_' + str(worker_id)]
            )
        )

    return dummy_worker
