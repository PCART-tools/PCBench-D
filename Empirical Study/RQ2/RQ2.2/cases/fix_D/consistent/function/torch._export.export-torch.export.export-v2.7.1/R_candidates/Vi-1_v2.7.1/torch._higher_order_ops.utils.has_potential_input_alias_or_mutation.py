def has_potential_input_alias_or_mutation(gm, inputs, pre_dispatch=False):
    try:
        gm = _maybe_fake_tracing(gm, inputs, pre_dispatch)
    except UnsupportedAliasMutationException:
        # this can happen when nested cond_op is
        # functionalized
        return True
    except Exception as e:
        raise e

    return _detect_input_mutation(gm) or _detect_input_alias(gm)
