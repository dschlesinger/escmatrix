from escmatrix import EscapeColor, HexColor, CustomHex
from pydantic import ValidationError

def test_custom_hex() -> None:

    are_hex = ['#aFaFaF', '#000', "#1F7597", '#890282', '#eeeeee', '#00FFaa']
    not_hex = ['#aaaaa', '#plant', 'aaa', 'aaaaaa', 'AAA', 'AAADDD']

    # Are hexcode, should not error
    for a in are_hex:

        try:
            c = CustomHex(hex_code=a)

            c("Hello World")

        except ValidationError as ve:
            raise AssertionError(f'Valid hex code {a} falid validation')

    # Not hex should error
    for n in not_hex:
        try:
            CustomHex(hex_code=n)

            # Shoud not get here
            raise AssertionError(f'Non valid hex code {n} passed')
        except ValidationError as ve:
            # Should happen

            pass