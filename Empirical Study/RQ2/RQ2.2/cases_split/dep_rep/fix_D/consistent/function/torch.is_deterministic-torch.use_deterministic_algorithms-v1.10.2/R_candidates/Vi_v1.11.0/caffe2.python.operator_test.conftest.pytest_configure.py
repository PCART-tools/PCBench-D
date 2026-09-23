def pytest_configure(config):
    generate = config.getoption('generate', default=False)
    output = config.getoption('output', default=serial.DATA_DIR)
    disable = config.getoption('disable', default=False)
    disable_coverage = config.getoption('disable_coverage', default=False)
    serial._output_context.__setattr__('should_generate_output', generate)
    serial._output_context.__setattr__('output_dir', output)
    serial._output_context.__setattr__('disable_serialized_check', disable)
    serial._output_context.__setattr__('disable_gen_coverage', disable_coverage)
