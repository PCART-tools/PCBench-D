@pytest.mark.parametrize('module_name', module_names)
@pytest.mark.filterwarnings('ignore::DeprecationWarning')
def test_getattr(module_name):
    """
    Test that __getattr__ methods raise AttributeError for unknown keys.
    See #20822, #20855.
    """
    try:
        module = import_module(module_name)
    except (ImportError, RuntimeError) as e:
        # Skip modules that cannot be imported due to missing dependencies
        pytest.skip(f'Cannot import {module_name} due to {e}')

    key = 'THIS_SYMBOL_SHOULD_NOT_EXIST'
    if hasattr(module, key):
        delattr(module, key)
