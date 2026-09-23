@contextlib.contextmanager
def exporter_context(model, mode):
    with select_model_mode_for_export(model, mode) as mode_ctx, \
            disable_apex_o2_state_dict_hook(model) as apex_ctx:
        yield (mode_ctx, apex_ctx)
