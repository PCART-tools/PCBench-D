  def assertMultiLineStrippedEqual(self, expected, what):
    """Asserts two strings are equal, after dedenting and stripping each line."""
    expected = textwrap.dedent(expected)
    what = textwrap.dedent(what)
    ignore_space_re = re.compile(r'\s*\n\s*')
    expected_clean = re.sub(ignore_space_re, '\n', expected.strip())
    what_clean = re.sub(ignore_space_re, '\n', what.strip())
    if what_clean != expected_clean:
      # Print it so we can copy-and-paste it into the test
      print(f"Found\n{what}\n")
    self.assertMultiLineEqual(expected_clean, what_clean,
                              msg=f"Found\n{what}\nExpecting\n{expected}")
