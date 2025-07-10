from enum import Enum
import re, string

from pydantic import validate_call, computed_field, AfterValidator, ValidationError
from typing import Annotated, Set

POSSIBLE_HEX_CHAR: Set[str] = set([*string.ascii_lowercase[0:6]] + [*string.ascii_uppercase[0:6]] + [str(n) for n in range(10)])

def is_hex_code(hex_code: str) -> str:
    """Format should be #......
    Lower or upper, stored as lower
    """

    if hex_code[0] != '#':

        raise ValidationError('Hex code must start with #')
    
    if len(hex_code) not in [4, 7]:

        raise ValidationError('Hex code must be 4 or 7 chars, does not support alpha')
    
    for c in hex_code:

        if c not in POSSIBLE_HEX_CHAR:

            raise ValidationError(f'Char {c} is not a valid hex char')

    return hex_code.lower()

HexCode = Annotated[str, AfterValidator(is_hex_code)]

class EscapeColor(Enum):

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    RESET = "\033[0m"

    @validate_call
    def __call__(self, text: str) -> None:

        print(self.apply(text))

    @validate_call
    def apply(self, text: str) -> str:

        return f'{self.value}{text}{EscapeColor.RESET.value}'

class HexColor(Enum):
    RED     = "#FF0000"
    GREEN   = "#00FF00"
    BLUE    = "#0000FF"
    YELLOW  = "#FFFF00"
    CYAN    = "#00FFFF"
    MAGENTA = "#FF00FF"
    BLACK   = "#000000"
    WHITE   = "#FFFFFF"

    @validate_call
    def __call__(self, text: str) -> None:

        print(self.apply(text))

    @validate_call
    def apply(self, text: str) -> str:

        return f'{self.value}{text}{EscapeColor.RESET.value}'
    
    @computed_field
    @property
    def escape(self) -> str:

        return 'Hello'