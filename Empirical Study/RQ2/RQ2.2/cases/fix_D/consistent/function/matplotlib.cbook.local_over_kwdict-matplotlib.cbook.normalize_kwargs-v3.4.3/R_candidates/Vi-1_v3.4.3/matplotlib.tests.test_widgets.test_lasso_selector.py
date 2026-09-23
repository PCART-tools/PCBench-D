def test_lasso_selector():
    check_lasso_selector()
    check_lasso_selector(useblit=False, lineprops=dict(color='red'))
    check_lasso_selector(useblit=True, button=1)
