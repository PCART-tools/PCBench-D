@contextlib.contextmanager
def sanitize_gm_for_cache(gm: torch.fx.GraphModule):
    """
    Clears a few fields in a dynamo supplied Graph Module that are not stable between graph inputs, but don't
    affect inductor or aotdispatch correctness.

    These fields **can** be used by code calling into aotdispatch (namely, dynamo), so we can't null them out completely.

    To ensure that these fields are not accessed by inductor or aotdispatch, we clear them during AOTAutogradCache.load,
    and then put them back before returning. This way, we generate a cache key based off of a canonical graph
    without these fields, and also guarantee they aren't used to affect the cache's output.
    """
    IGNORED_FIELDS = (
        "meta",  # metadata used by export
        "compile_subgraph_reason",  # Used by dynamo only for logging, no change in inductor/autograd behavior
        "_param_name_to_source",  # Encapsulated by aot_config.aot_autograd_arg_pos_to_source
        "_backend_id",
    )
    saved_fields = {}
    for field in IGNORED_FIELDS:
        saved_fields[field] = getattr(gm, field, None)
        # Clear the field
        setattr(gm, field, None)
    try:
        yield
    finally:
        # Put the fields back after dispatch_and_compile is complete
        for field, value in saved_fields.items():
            setattr(gm, field, value)
