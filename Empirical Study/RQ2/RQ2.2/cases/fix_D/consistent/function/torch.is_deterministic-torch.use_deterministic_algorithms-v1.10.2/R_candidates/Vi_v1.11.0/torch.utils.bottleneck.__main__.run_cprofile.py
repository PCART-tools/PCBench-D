def run_cprofile(code, globs, launch_blocking=False):
    print('Running your script with cProfile')
    prof = cProfile.Profile()
    prof.enable()
    exec(code, globs, None)
    prof.disable()
    return prof
