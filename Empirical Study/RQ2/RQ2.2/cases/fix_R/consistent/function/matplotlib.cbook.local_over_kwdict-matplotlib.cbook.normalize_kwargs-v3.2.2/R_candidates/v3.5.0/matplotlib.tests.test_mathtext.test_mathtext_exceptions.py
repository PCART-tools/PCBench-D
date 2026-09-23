@pytest.mark.parametrize(
    'math, msg',
    [
        (r'$\hspace{}$', r'Expected \hspace{n}'),
        (r'$\hspace{foo}$', r'Expected \hspace{n}'),
        (r'$\frac$', r'Expected \frac{num}{den}'),
        (r'$\frac{}{}$', r'Expected \frac{num}{den}'),
        (r'$\binom$', r'Expected \binom{num}{den}'),
        (r'$\binom{}{}$', r'Expected \binom{num}{den}'),
        (r'$\genfrac$',
         r'Expected \genfrac{ldelim}{rdelim}{rulesize}{style}{num}{den}'),
        (r'$\genfrac{}{}{}{}{}{}$',
         r'Expected \genfrac{ldelim}{rdelim}{rulesize}{style}{num}{den}'),
        (r'$\sqrt$', r'Expected \sqrt{value}'),
        (r'$\sqrt f$', r'Expected \sqrt{value}'),
        (r'$\overline$', r'Expected \overline{value}'),
        (r'$\overline{}$', r'Expected \overline{value}'),
        (r'$\leftF$', r'Expected a delimiter'),
        (r'$\rightF$', r'Unknown symbol: \rightF'),
        (r'$\left(\right$', r'Expected a delimiter'),
        # PyParsing 2 uses double quotes, PyParsing 3 uses single quotes and an
        # extra backslash.
        (r'$\left($', re.compile(r'Expected ("|\'\\)\\right["\']')),
        (r'$\dfrac$', r'Expected \dfrac{num}{den}'),
        (r'$\dfrac{}{}$', r'Expected \dfrac{num}{den}'),
        (r'$\overset$', r'Expected \overset{body}{annotation}'),
        (r'$\underset$', r'Expected \underset{body}{annotation}'),
    ],
    ids=[
        'hspace without value',
        'hspace with invalid value',
        'frac without parameters',
        'frac with empty parameters',
        'binom without parameters',
        'binom with empty parameters',
        'genfrac without parameters',
        'genfrac with empty parameters',
        'sqrt without parameters',
        'sqrt with invalid value',
        'overline without parameters',
        'overline with empty parameter',
        'left with invalid delimiter',
        'right with invalid delimiter',
        'unclosed parentheses with sizing',
        'unclosed parentheses without sizing',
        'dfrac without parameters',
        'dfrac with empty parameters',
        'overset without parameters',
        'underset without parameters',
    ]
)
def test_mathtext_exceptions(math, msg):
    parser = mathtext.MathTextParser('agg')
    match = re.escape(msg) if isinstance(msg, str) else msg
    with pytest.raises(ValueError, match=match):
        parser.parse(math)
