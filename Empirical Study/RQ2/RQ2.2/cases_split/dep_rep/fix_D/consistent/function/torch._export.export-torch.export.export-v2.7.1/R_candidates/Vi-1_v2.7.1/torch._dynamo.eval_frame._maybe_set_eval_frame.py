def _maybe_set_eval_frame(callback: DynamoCallback):
    # A wrapper on set_eval_frame that is guarded by a Justknob.
    # Users can disable torchDynamo by setting the JK to False.
    if not justknobs_check("pytorch/compiler:enable_compiler_set_eval_frame"):
        torch._dynamo.utils.warn_once(
            "Dynamo disabled by Justknob: enable_compiler_set_eval_frame, skipping set_eval_frame"
        )
        return callback
    else:
        return set_eval_frame(callback)
