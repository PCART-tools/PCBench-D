def _infer_shapes(pred_net, inputs):
    workspace.RunNetOnce(pred_net)
    hints = {}
    for op in pred_net.op:
        for o in op.output:
            if o not in hints:
                blob = workspace.FetchBlob(o)
                if hasattr(blob, 'shape'):
                    hints[o] = blob.shape
        for i in op.input:
            if i not in hints:
                blob = workspace.FetchBlob(i)
                if hasattr(blob, 'shape'):
                    hints[i] = blob.shape

    return hints
