"""
This is one of the solutions we came up with while discussing the qualifier
with staff. It's not the most efficient solution, just one that solves all
the requirements in a staightforward manner.

The `README.md` in this folder contains annotations that explain why we
coded it this way.
"""
import itertools
import random
import string

from typing import Iterable, Optional


def generate_password(
    password_length: int = 8,
    has_symbols: bool = False,
    has_uppercase: bool = False,
    ignored_chars: Optional[Iterable[str]] = None,
    allowed_chars: Optional[Iterable[str]] = None
) -> str:
    """
    Generates a random password.

    `password_length`: length of the generated password (max: 1,000,000,000)
    `has_symbols`: if True, the password will contain at least one symbol
    `has_uppercase`: if True, the password will contain at least one uppercase character
    `ignored_chars`: An optional iterable of characters that should not be used
    `allowed_chars`: An optional iterable specifying the characters to be used

    Note: The options `ignored_chars` and `allowed_chars` cannot be used together
    """
    if ignored_chars and allowed_chars:
        raise UserWarning("`ignored_chars` and `allowed_chars` cannot be set at the same time")

    # If both `has_uppercase` and `has_symbols` are set, we need `password_length` >= 2
    minimum_length = max(1, has_uppercase + has_symbols)
    if minimum_length > password_length:
        raise UserWarning(
            f"`password_length` must be at least {minimum_length} for the specified options."
        )

    # Let's ensure that the algorithm finishes in a reasonable amount of time
    if password_length > 1_000_000_000:
        raise UserWarning(f"The maximum `password_length` is 1,000,000,000")

    numbers = string.digits
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    symbols = string.punctuation

    if ignored_chars:
        # Create a new set object from a potentially exhaustible iterable, like an iterator
        ignored_chars = set(ignored_chars)

        numbers = [char for char in numbers if char not in ignored_chars]
        lowercase = [char for char in lowercase if char not in ignored_chars]
        uppercase = [char for char in uppercase if char not in ignored_chars]
        symbols = [char for char in symbols if char not in ignored_chars]

    if allowed_chars:
        allowed_chars = set(allowed_chars)

        symbols = [char for char in symbols if char in allowed_chars]
        uppercase = [char for char in uppercase if char in allowed_chars]

        pool = list(allowed_chars)
    else:
        # We need a subscriptable object for `random.choices`
        pool = list(itertools.chain(lowercase, uppercase, numbers, symbols))

    password = random.choices(pool, k=password_length)

    # If `has_symbols` or `has_uppercase` were set, we will ensure those characters by replacing
    # a random character in the password by a random uppercase and/or symbol. Here we draw the
    # number of indices required for the replacements.
    indices = random.sample(range(password_length), has_uppercase + has_symbols)

    if has_symbols:
        if not symbols:
            raise UserWarning(
                "`has_symbols` was set, but the character set did not contain symbols"
            )
        password[indices[0]] = random.choice(symbols)

    if has_uppercase:
        if not uppercase:
            raise UserWarning(
                "`has_uppercase` was set, but the character set did not contain uppercase letters"
            )
        # If `has_symbols` was also set, take the second index, otherwise the first.
        password[indices[0 + has_symbols]] = random.choice(uppercase)

    return "".join(password)
