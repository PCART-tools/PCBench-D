def test_mathtext_fallback_to_cm_invalid():
    for fallback in [True, False]:
        with pytest.warns(_api.MatplotlibDeprecationWarning):
            mpl.rcParams['mathtext.fallback_to_cm'] = fallback
