def _rref_typeof_on_user(rref, timeout=UNSET_RPC_TIMEOUT, blocking=True):
    fut = rpc_async(
        rref.owner(),
        _rref_typeof_on_owner,
        args=(rref,),
        timeout=timeout
    )
    if blocking:
        return fut.wait()
    else:
        return fut
