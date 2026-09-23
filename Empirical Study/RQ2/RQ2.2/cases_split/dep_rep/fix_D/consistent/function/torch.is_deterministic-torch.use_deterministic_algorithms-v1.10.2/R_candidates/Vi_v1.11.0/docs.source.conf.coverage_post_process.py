def coverage_post_process(app, exception):
    if exception is not None:
        return

    # Only run this test for the coverage build
    if not isinstance(app.builder, CoverageBuilder):
        return

    # These are all the modules that have "automodule" in an rst file
    # These modules are the ones for which coverage is checked
    # Here, we make sure that no module is missing from that list
    modules = app.env.domaindata['py']['modules']

    # We go through all the torch submodules and make sure they are
    # properly tested
    missing = set()

    def is_not_internal(modname):
        split_name = modname.split(".")
        for name in split_name:
            if name[0] == "_":
                return False
        return True

    # The walk function does not return the top module
    if "torch" not in modules:
        missing.add("torch")

    for _, modname, ispkg in pkgutil.walk_packages(path=torch.__path__,
                                                   prefix=torch.__name__ + '.'):
        if ispkg and is_not_internal(modname):
            if modname not in modules:
                missing.add(modname)

    expected = set(coverage_missing_automodule)

    output = []

    unexpected_missing = missing - expected
    if unexpected_missing:
        mods = ", ".join(unexpected_missing)
        output.append(f"\nYou added the following module(s) to the PyTorch namespace '{mods}' "
                      "but they have no corresponding entry in a doc .rst file. You should "
                      "either make sure that the .rst file that contains the module's documentation "
                      "properly contains either '.. automodule:: mod_name' (if you do not want "
                      "the paragraph added by the automodule, you can simply use py:module) or "
                      "make the module private (by appending an '_' at the beginning of its name.")

    unexpected_not_missing = expected - missing
    if unexpected_not_missing:
        mods = ", ".join(unexpected_not_missing)
        output.append(f"\nThank you for adding the missing .rst entries for '{mods}', please update "
                      "the 'coverage_missing_automodule' in 'torch/docs/source/conf.py' to remove "
                      "the module(s) you fixed and make sure we do not regress on this in the future.")

    # The output file is hard-coded by the coverage tool
    # Our CI is setup to fail if any line is added to this file
    output_file = path.join(app.outdir, 'python.txt')

    if output:
        with open(output_file, "a") as f:
            for o in output:
                f.write(o)
