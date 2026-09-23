def test_data_parameter_replacement():
    """
    Test that that the docstring contains the correct *data* parameter stub
    for all methods that we run _preprocess_data() on.
    """
    program = (
        "import logging; "
        "logging.basicConfig(level=logging.DEBUG); "
        "import matplotlib.pyplot as plt"
    )
    cmd = [sys.executable, "-c", program]
    completed_proc = subprocess.run(cmd, text=True, capture_output=True)
    assert 'data parameter docstring error' not in completed_proc.stderr
