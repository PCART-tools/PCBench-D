def fun_conclude_operator(self):
    # Ensure the program exists. This is to "fix" some unknown problems
    # causing the job sometimes get stuck.
    timeout_guard.EuthanizeIfNecessary(600.0)
