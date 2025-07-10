from escmatrix.color import is_hex_code
from pydantic import ValidationError

def test_is_hex_code() -> None:

    are_hex = ['#AAA', '#000', '#BA65E5', '#890282', '#eeeeee']
    not_hex = ['#aaaaa', '#plant', 'aaa', 'aaaaaa', 'AAA', 'AAADDD']

    # Are hexcode, should not error
    for a in are_hex:

        try:
            is_hex_code(a)
        except ValidationError as ve:
            raise AssertionError(f'Valid hex code {a} falid validation')

    # Not hex should error
    for n in not_hex:
        try:
            is_hex_code(n)

            # Shoud not get here
            raise AssertionError(f'Non valid hex code {n} passed')
        except ValidationError as ve:
            # Should happen

            pass