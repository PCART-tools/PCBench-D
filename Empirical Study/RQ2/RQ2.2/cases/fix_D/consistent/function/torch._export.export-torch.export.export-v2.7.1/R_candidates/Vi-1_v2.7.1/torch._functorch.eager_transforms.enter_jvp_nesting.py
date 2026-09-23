def enter_jvp_nesting():
    global JVP_NESTING
    jvp_level = _jvp_increment_nesting()
    JVP_NESTING += 1
    return jvp_level
