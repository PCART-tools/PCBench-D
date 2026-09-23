def exit_jvp_nesting():
    global JVP_NESTING
    _jvp_decrement_nesting()
    JVP_NESTING -= 1
