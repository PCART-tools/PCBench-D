@contextlib.contextmanager
def dynamo_under_activation_checkpoint(tx: "InstructionTranslator"):
    orig_val = tx.output.current_tracer.under_activation_checkpoint
    try:
        tx.output.current_tracer.under_activation_checkpoint = True
        yield
    finally:
        tx.output.current_tracer.under_activation_checkpoint = orig_val
