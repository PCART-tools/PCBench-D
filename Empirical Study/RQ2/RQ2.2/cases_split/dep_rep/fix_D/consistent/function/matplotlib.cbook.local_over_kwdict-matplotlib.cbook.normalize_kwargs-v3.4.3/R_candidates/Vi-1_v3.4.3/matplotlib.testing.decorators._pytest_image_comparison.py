def _pytest_image_comparison(baseline_images, extensions, tol,
                             freetype_version, remove_text, savefig_kwargs,
                             style):
    """
    Decorate function with image comparison for pytest.

    This function creates a decorator that wraps a figure-generating function
    with image comparison code.
    """
    import pytest

    extensions = map(_mark_skip_if_format_is_uncomparable, extensions)
    KEYWORD_ONLY = inspect.Parameter.KEYWORD_ONLY

    def decorator(func):
        old_sig = inspect.signature(func)

        @functools.wraps(func)
        @pytest.mark.parametrize('extension', extensions)
        @pytest.mark.style(style)
        @_checked_on_freetype_version(freetype_version)
        @functools.wraps(func)
        def wrapper(*args, extension, request, **kwargs):
            __tracebackhide__ = True
            if 'extension' in old_sig.parameters:
                kwargs['extension'] = extension
            if 'request' in old_sig.parameters:
                kwargs['request'] = request

            img = _ImageComparisonBase(func, tol=tol, remove_text=remove_text,
                                       savefig_kwargs=savefig_kwargs)
            matplotlib.testing.set_font_settings_for_testing()
            func(*args, **kwargs)

            # If the test is parametrized in any way other than applied via
            # this decorator, then we need to use a lock to prevent two
            # processes from touching the same output file.
            needs_lock = any(
                marker.args[0] != 'extension'
                for marker in request.node.iter_markers('parametrize'))

            if baseline_images is not None:
                our_baseline_images = baseline_images
            else:
                # Allow baseline image list to be produced on the fly based on
                # current parametrization.
                our_baseline_images = request.getfixturevalue(
                    'baseline_images')

            assert len(plt.get_fignums()) == len(our_baseline_images), (
                "Test generated {} images but there are {} baseline images"
                .format(len(plt.get_fignums()), len(our_baseline_images)))
            for idx, baseline in enumerate(our_baseline_images):
                img.compare(idx, baseline, extension, _lock=needs_lock)

        parameters = list(old_sig.parameters.values())
        if 'extension' not in old_sig.parameters:
            parameters += [inspect.Parameter('extension', KEYWORD_ONLY)]
        if 'request' not in old_sig.parameters:
            parameters += [inspect.Parameter("request", KEYWORD_ONLY)]
        new_sig = old_sig.replace(parameters=parameters)
        wrapper.__signature__ = new_sig

        # Reach a bit into pytest internals to hoist the marks from our wrapped
        # function.
        new_marks = getattr(func, 'pytestmark', []) + wrapper.pytestmark
        wrapper.pytestmark = new_marks

        return wrapper

    return decorator
