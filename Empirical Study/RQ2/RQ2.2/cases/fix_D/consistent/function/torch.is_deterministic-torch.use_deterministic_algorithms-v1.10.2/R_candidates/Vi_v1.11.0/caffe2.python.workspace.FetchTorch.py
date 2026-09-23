def FetchTorch(name):
    ws = C.Workspace.current
    return ws.blobs[name].to_torch()
