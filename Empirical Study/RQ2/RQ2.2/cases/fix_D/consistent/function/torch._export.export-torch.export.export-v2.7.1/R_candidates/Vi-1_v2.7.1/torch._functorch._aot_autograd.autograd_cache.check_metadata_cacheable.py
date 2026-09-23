def check_metadata_cacheable(metadata: ViewAndMutationMeta):
    """
    When view replay is turned on, we bypass autograd cache if
    the output is aliased.
    """
    if config.view_replay_for_aliased_outputs:
        for info in metadata.output_info:
            if info.functional_tensor is not None:
                raise BypassAOTAutogradCache(
                    "Cannot cache a graph with functional tensor"
                )
