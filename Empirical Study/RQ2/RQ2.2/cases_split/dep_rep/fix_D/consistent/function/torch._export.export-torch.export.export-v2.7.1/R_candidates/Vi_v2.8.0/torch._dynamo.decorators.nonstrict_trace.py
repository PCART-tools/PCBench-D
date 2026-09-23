def nonstrict_trace(traceable_fn):
    # Like `allow_in_graph`, but with the following enhancements/differences:
    #
    # 1. Supports user-defined class as inputs, as long as the class has been
    #    registered with pytree.
    # 2. Reads to global/captured tensors forces the underlying graph to treat
    #    those tensors as constant, and we _assume_ they will not be updated. This
    #    is similar to FX tracing.
    # 3. In the resulting Dynamo graph, the call to a `nonstrict_trace`-ed function
    #    will be represented as a call to `torch._higher_order_ops.flat_apply`,
    #    which takes in the `nonstrict_trace`-ed function and pytree-flattened
    #    inputs.
    # 4. Only the returned function is traceable, and the original function will
    #    not be. Moreover, `nonstrict_trace` can be used inside a `torch.compile`
    #    region.
    #
    # NOTE: like `allow_in_graph`, aliasing information is neither preserved
    # between inputs themselves, nor between inputs and outputs.
    assert callable(traceable_fn), "nonstrict_trace expects a callable"

    @functools.wraps(traceable_fn)
    def wrapped(*args, **kwargs):
        return traceable_fn(*args, **kwargs)

    wrapped_id = id(wrapped)

    # This line allows us to reuse much of the `allow_in_graph` impl.
    trace_rules._allowed_callable_ids.add(wrapped_id)

    # This line allows us to diverge the impl from `allow_in_graph`.
    trace_rules._nonstrict_trace_callable_ids.add(wrapped_id)

    # Avoid id reuse which creates subtle bugs.
    def deregister():
        trace_rules._allowed_callable_ids.remove(wrapped_id)
        trace_rules._nonstrict_trace_callable_ids.remove(wrapped_id)

    weakref.finalize(wrapped, deregister)

    return wrapped
