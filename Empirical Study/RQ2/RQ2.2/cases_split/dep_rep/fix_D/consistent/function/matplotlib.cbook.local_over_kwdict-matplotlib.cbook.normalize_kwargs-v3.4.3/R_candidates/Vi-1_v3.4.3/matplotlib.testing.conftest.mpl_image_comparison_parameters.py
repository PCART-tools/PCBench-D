@pytest.fixture
def mpl_image_comparison_parameters(request, extension):
    # This fixture is applied automatically by the image_comparison decorator.
    #
    # The sole purpose of this fixture is to provide an indirect method of
    # obtaining parameters *without* modifying the decorated function
    # signature. In this way, the function signature can stay the same and
    # pytest won't get confused.
    # We annotate the decorated function with any parameters captured by this
    # fixture so that they can be used by the wrapper in image_comparison.
    baseline_images, = request.node.get_closest_marker('baseline_images').args
    if baseline_images is None:
        # Allow baseline image list to be produced on the fly based on current
        # parametrization.
        baseline_images = request.getfixturevalue('baseline_images')

    func = request.function
    with cbook._setattr_cm(func.__wrapped__,
                           parameters=(baseline_images, extension)):
        yield
