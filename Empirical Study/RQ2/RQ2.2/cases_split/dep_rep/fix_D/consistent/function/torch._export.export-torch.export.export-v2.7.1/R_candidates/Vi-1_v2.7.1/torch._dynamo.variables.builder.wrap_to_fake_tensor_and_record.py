def wrap_to_fake_tensor_and_record(
    e, tx, *, source: Optional[Source], is_tensor: bool, parent_context=None
):
    if (
        type(e) in (torch.Tensor, torch.nn.Parameter, FakeTensor)
        or isinstance(e, torch.Tensor)
        or is_traceable_wrapper_subclass(e)
    ):
        assert source is not None
        static_shapes, _reason = tensor_always_has_static_shape(
            e,
            is_tensor,
            tensor_source=source,
        )

        if not parent_context:
            symbolic_context = _automatic_dynamic(e, tx, source, static_shapes)
        else:
            # Parent contexts are passed in when we are recursively creating
            # fake tensors for subclasses. A better design would be not to create a
            # parent/child relationship, but to recursively call _automatic_dynamic
            # as we recursively call wrap_to_fake_tensor_and_record. This runs
            # into bugs around how meta_utils knows and works to create fake tensors
            # with tensor subclasses. Ideally, dynamo would drive both the recursive
            # wrap_to_fake_tensor_and_record and _automatic_dynamic policy creation.
            assert isinstance(source, AttrSource)
            inner_context_name = source.member
            symbolic_context = parent_context.inner_contexts[inner_context_name]

        log.debug(
            "wrap_to_fake %s %s %s %s",
            source.name(),
            tuple(e.shape),
            symbolic_context,
            type(e),
        )
        fake_e = wrap_fake_exception(
            lambda: tx.fake_mode.from_tensor(
                e,
                source=source,
                symbolic_context=symbolic_context,
            )
        )
        if (
            source is not None
            and isinstance(fake_e, FakeTensor)
            and (sym_val := fake_e.item_memo) is not None
        ):
            tx.output.tracked_fakes.append(
                TrackedFake(sym_val, CallMethodItemSource(source), symbolic_context)
            )

        if is_traceable_wrapper_subclass(fake_e):
            attrs, _ = fake_e.__tensor_flatten__()
            for attr in attrs:
                fake_inner = getattr(fake_e, attr)
                inner = getattr(e, attr)
                inner_source = AttrSource(source, attr)
                wrap_to_fake_tensor_and_record(
                    inner,
                    tx,
                    source=inner_source,
                    is_tensor=isinstance(fake_inner, torch.Tensor),
                    parent_context=symbolic_context,
                )

        tx.output.tracing_context.tensor_to_context[e] = symbolic_context
        if is_sparse_any(fake_e):
            # TODO: for TensorGuards, this eventually may need more
            #       fields for the size/stride of any other constituents
            values = fake_e._values() if fake_e.is_sparse else fake_e.values()
            tx.output.input_source_to_sizes_strides[source] = {
                "size": fake_e.size(),
                # TODO: revise this, but for now this stride instead of ()
                #       avoids SegFault with PYTORCH_TEST_WITH_DYNAMO=1
                "stride": (1,) * fake_e.ndim,
                "values_size": values.size(),
                "values_stride": values.stride(),
            }
        else:
            tx.output.input_source_to_sizes_strides[source] = {
                "size": fake_e.size(),
                "stride": fake_e.stride(),
            }

        if (
            is_tensor
            and not (static_shapes and source.is_specialized_nn_module())
            and not is_constant_source(source)
        ):
            tx.output.tracked_fakes.append(
                TrackedFake(fake_e, source, symbolic_context)
            )
            tx.output.tracked_fakes_id_to_source[id(e)].append(source)

        return fake_e
    else:
        return e
