def blob_nbytes(blob):
    sz = 0
    try:
        sz = workspace.FetchBlob(blob).nbytes
    except Exception:
        log.warning('Error when fetching blob {}'.format(blob))
    return sz
