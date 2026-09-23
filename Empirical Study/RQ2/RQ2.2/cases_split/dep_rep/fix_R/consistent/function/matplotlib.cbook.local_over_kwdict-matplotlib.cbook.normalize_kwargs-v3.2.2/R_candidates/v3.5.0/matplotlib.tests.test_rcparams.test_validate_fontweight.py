@pytest.mark.parametrize('weight, parsed_weight', [
    ('bold', 'bold'),
    ('BOLD', ValueError),  # weight is case-sensitive
    (100, 100),
    ('100', 100),
    (np.array(100), 100),
    # fractional fontweights are not defined. This should actually raise a
    # ValueError, but historically did not.
    (20.6, 20),
    ('20.6', ValueError),
    ([100], ValueError),
])
def test_validate_fontweight(weight, parsed_weight):
    if parsed_weight is ValueError:
        with pytest.raises(ValueError):
            validate_fontweight(weight)
    else:
        assert validate_fontweight(weight) == parsed_weight
