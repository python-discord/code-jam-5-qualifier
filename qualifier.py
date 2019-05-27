def generate_password(password_length: int = 8, has_symbols: bool = False, has_uppercase: bool = False):
    """Generates a random password.

    The password will be exactly `password_length` characters.
    If `has_symbols` is True, the password will contain at least one symbol, such as #, !, or @.
    If `has_uppercase` is True, the password will contain at least one upper case letter.
    """
