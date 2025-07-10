from enum import Enum
import re, string

from pydantic import validate_call, computed_field, AfterValidator, \
                    ValidationError, field_validator, BaseModel
from typing import Annotated, Set

POSSIBLE_HEX_CHAR: Set[str] = set("0123456789abcdefABCDEF")

@validate_call
def is_hex_code(hex_code: str) -> str:
            """Format should be #......
            Lower or upper, stored as lower
            """

            if hex_code[0] != '#':

                raise ValueError('Hex code must start with #')
            
            if len(hex_code) not in [4, 7]:

                raise ValueError('Hex code must be 4 or 7 chars, does not support alpha')
            
            for c in hex_code[1:]:

                if c not in POSSIBLE_HEX_CHAR:

                    raise ValueError(f'Char {c} is not a valid hex char')

            return hex_code.upper()

@validate_call
def hex_to_escape(hex_code: str) -> str:

            h = hex_code

            single = len(h) == 4

            if single:

                r, g, b = [str(int(c, base=16)) for c in h[1:]]
            
            else:

                r, g, b = [str(int(c, base=16)) for c in [h[1:3], h[3: 5], h[5: 7]]]

            return ';'.join([r, g, b])

class ColorBackground:

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

            return f'\033[48;2;{self.escape}m{text}{ColorText.EscapeColor.RESET.value}'
        
        @computed_field
        @property
        def escape(self) -> str:

            return hex_to_escape(self.value)
        
    class CustomHex(BaseModel):

        hex_code: str

        @field_validator('hex_code', mode='after')
        @classmethod
        def is_hex_code_wrapper(cls, hex_code: str) -> str:
            return is_hex_code(hex_code)

        @validate_call
        def __call__(self, text: str) -> None:

            print(self.apply(text))

        @validate_call
        def apply(self, text: str) -> str:

            return f'\033[48;2;{self.escape}m{text}{ColorText.EscapeColor.RESET.value}'
        
        @computed_field
        @property
        def escape(self) -> str:

            return hex_to_escape(self.hex_code)

class ColorText:
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

            return f'{self.value}{text}{ColorText.EscapeColor.RESET.value}'

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

            return f'\033[38;2;{self.escape}m{text}{ColorText.EscapeColor.RESET.value}'
        
        @computed_field
        @property
        def escape(self) -> str:

            return hex_to_escape(self.value)
        
    class CustomHex(BaseModel):

        hex_code: str

        @field_validator('hex_code', mode='after')
        @classmethod
        def is_hex_code_wrapper(cls, hex_code: str) -> str:
            return is_hex_code(hex_code)

        @validate_call
        def __call__(self, text: str) -> None:

            print(self.apply(text))

        @validate_call
        def apply(self, text: str) -> str:

            return f'\033[38;2;{self.escape}m{text}{ColorText.EscapeColor.RESET.value}'
        
        @computed_field
        @property
        def escape(self) -> str:

            return hex_to_escape(self.hex_code)