def set_proxy_slot(
    obj: Union[PySymType, _AnyScriptObjectType, Tensor],
    tracer: _ProxyTracer,
    proxy: object,
) -> None:
    log.debug("set_proxy_slot %s (%s) %s", obj, id(obj), proxy)
    if isinstance(obj, Tensor):
        # We DO want to clobber proxies whenever we run an inplace operation
        # on a tensor, and it affects the metadata on the proxy.
        assert isinstance(proxy, _ProxyTensor)
        tracer.tensor_tracker[obj] = proxy
    elif isinstance(obj, (_AnyScriptObject)):
        # We DO want to clobber proxies, with a similar rationale as for tensors.
        assert isinstance(proxy, Proxy)
        tracer.script_object_tracker[obj] = proxy
    else:
        # NB: Never clobber pre-existing proxy.  Although the proxies
        # are in principle equivalent, when we do graph partitioning
        # we need there not to be spurious dependencies on tangent inputs.
        # This works because primals get their SymInts set first, and
        # THEN later we allocate tangent inputs.  Make sure if a SymInt
        # is derivable from a primal that we use that.
        assert isinstance(obj, py_sym_types), type(obj)
        if obj not in tracer.symnode_tracker:
            tracer.symnode_tracker[obj] = typing.cast(_PySymProxyType, proxy)

            # WAR: python test/dynamo/test_subclasses.py
            # TestNestedTensor.test_basic_autograd
            #
            # AOTAutograd doesn't pass the "outer sizes" as an actual argument
            # to make_fx, but it is made use of internally in AOTAutograd's
            # call to tensor unflatten.  Because the outer sizes isn't passed
            # as an argument, it is therefore untracked.  However, it turns
            # out you luck out, because *Dynamo* will manually add the outer
            # sizes as an argument so you can fix up the proxy'ness.
            #
            # This is probably fixed in
            # https://github.com/pytorch/pytorch/pull/125941/
            import sympy

            if isinstance(obj.node.expr, sympy.Symbol):
                tracer.sympy_expr_tracker[obj.node.expr] = proxy
