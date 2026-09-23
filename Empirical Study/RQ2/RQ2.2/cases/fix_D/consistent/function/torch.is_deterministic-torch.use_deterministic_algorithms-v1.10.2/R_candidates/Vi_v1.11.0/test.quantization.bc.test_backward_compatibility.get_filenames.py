def get_filenames(self, subname):
    # NB: we take __file__ from the module that defined the test
    # class, so we place the expect directory where the test script
    # lives, NOT where test/common_utils.py lives.
    module_id = self.__class__.__module__
    munged_id = remove_prefix(self.id(), module_id + ".")
    test_file = os.path.realpath(sys.modules[module_id].__file__)
    base_name = os.path.join(os.path.dirname(test_file),
                             "../serialized",
                             munged_id)

    subname_output = ""
    if subname:
        base_name += "_" + subname
        subname_output = " ({})".format(subname)

    input_file = base_name + ".input.pt"
    state_dict_file = base_name + ".state_dict.pt"
    scripted_module_file = base_name + ".scripted.pt"
    traced_module_file = base_name + ".traced.pt"
    expected_file = base_name + ".expected.pt"
    package_file = base_name + ".package.pt"
    get_attr_targets_file = base_name + ".get_attr_targets.pt"

    return input_file, state_dict_file, scripted_module_file, \
        traced_module_file, expected_file, package_file, get_attr_targets_file
