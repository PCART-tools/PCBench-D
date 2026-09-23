def requires_gloo():
    return sandcastle_skip_if(
        not c10d.is_gloo_available(),
        "c10d was not compiled with the Gloo backend",
    )
