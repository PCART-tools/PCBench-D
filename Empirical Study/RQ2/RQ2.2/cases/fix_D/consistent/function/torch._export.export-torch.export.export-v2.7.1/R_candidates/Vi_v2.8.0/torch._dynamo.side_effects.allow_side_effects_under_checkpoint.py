@contextlib.contextmanager
def allow_side_effects_under_checkpoint(tx: "InstructionTranslator"):
    assert tx.output.current_tracer.under_activation_checkpoint
    orig_val = tx.output.current_tracer.allow_side_effects_under_checkpoint
    try:
        tx.output.current_tracer.allow_side_effects_under_checkpoint = True
        yield
    finally:
        tx.output.current_tracer.allow_side_effects_under_checkpoint = orig_val
