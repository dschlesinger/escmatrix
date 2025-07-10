from escmatrix import EscapeColor, HexColor, CustomHex, BgCustomHex, BgHexColor
from pydantic import ValidationError

def test_hex_background() -> None:

    BgHexColor.RED('Hello World')
    BgHexColor.BLUE('Hello World')
    BgHexColor.GREEN('Hello World')
    BgHexColor.YELLOW('Hello World')

    are_hex = ['#aFaFaF', '#000', "#1F7597", '#890282', '#eeeeee', '#00FFaa']
    not_hex = ['#aaaaa', '#plant', 'aaa', 'aaaaaa', 'AAA', 'AAADDD']

    # Are hexcode, should not error
    for a in are_hex:

        try:
            c = BgCustomHex(hex_code=a)

            c("Hello World")

        except ValidationError as ve:
            raise AssertionError(f'Valid hex code {a} falid validation')

    # Not hex should error
    for n in not_hex:
        try:
            BgCustomHex(hex_code=n)

            # Shoud not get here
            raise AssertionError(f'Non valid hex code {n} passed')
        except ValidationError as ve:
            # Should happen

            pass

def test_custom_hex() -> None:

    EscapeColor.RED('Hello World')
    EscapeColor.BLUE('Hello World')
    EscapeColor.GREEN('Hello World')
    EscapeColor.YELLOW('Hello World')

    HexColor.RED('Hello World')
    HexColor.BLUE('Hello World')
    HexColor.GREEN('Hello World')
    HexColor.YELLOW('Hello World')

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

def test_hex_background_and_color() -> None:

    text: str = 'Hello World'

    BgHexColor.RED(
        CustomHex(hex_code='#00FFFF').apply(text)
    )