import functools
import string
import timeit

from qualifier import generate_password


# Test if it completes in less than 5 seconds when generating a password with 999999 characters.
t = timeit.Timer(
    functools.partial(generate_password, 999999, True, True)
)

complete_time = t.timeit(1)

# Test if the function returns a string
returns_string = isinstance(generate_password(4), str)

# Test if it returns a password of the correct length
correct_length = len(generate_password(8)) == 8 and len(generate_password(162)) == 162

# Makes sure it returns a different random password each time
random_password = generate_password(32) != generate_password(32)

# Is the generator guaranteed to have symbols, if so instructed?
symbols_pass = generate_password(2, True)
has_symbols = any(letter in string.punctuation for letter in symbols_pass)

# Is the generator guaranteed to have uppercase letters, if so instructed?
uppercase_pass = generate_password(2, True, True)
has_uppercase = any(letter in string.ascii_uppercase for letter in uppercase_pass)

# Will ignored_chars be ignored?
try:
    ignored_chars = "b" not in generate_password(128000, ignored_chars=["b"])
except TypeError:
    # ignored_chars has not been implemented.
    ignored_chars = False

# Will anything but allowed chars be used?
try:
    allowed = ["A", "B", "C", "!"]
    allowed_chars = all(letter in allowed for letter in generate_password(128000, allowed_chars=allowed))
except TypeError:
    # allowed_chars has not been implemented.
    allowed_chars = False

# Does the generator raise a UserWarning if we provide both ignored_chars and allowed_chars?
try:
    generate_password(32, True, True, ["B"], ["b"])
    raises_user_warning = False

except Exception as e:
    raises_user_warning = isinstance(e, UserWarning)

# Returns a string
if returns_string:
    print("+ The function returns a string.")
else:
    print("- The function does not return a string.")

# Generates a password of correct length
if correct_length:
    print("+ The password generated was the correct length.")
else:
    print("- The password generated was of an incorrect length.")

# Generates a random password
if random_password:
    print("+ The implementation returns a different password with each call.")
else:
    print("- The implementation returned the same password across two separate calls.")

# Generates a password with symbols
if has_symbols:
    print(f"+ The password contained a symbol when required. The password generated was {symbols_pass}")
else:
    print(f"- The password did not contain a symbol when required. The password generated was {symbols_pass}")

# Generates a password with uppercase letters
if has_uppercase:
    print(f"+ The password contained an uppercase letter when required. The password generated was {uppercase_pass}")
else:
    print(
        "- The password did not contain an uppercase letter when required. "
        f"The password generated was {uppercase_pass}"
    )

# Raises UserWarning when expected to.
if raises_user_warning:
    print("+ The generator raises a UserWarning when both ignored and allowed chars are provided.")
else:
    print("- The generator does not raise a UserWarning when both ignored and allowed chars are provided.")

# Completes fast enough
if complete_time < 5.0:
    print(
        "+ When generating a password with 1 million characters, "
        f"the execution time was {complete_time:.2f} seconds."
    )
else:
    print(
        "- When generating a password with 1 million characters, "
        f"the execution time was {complete_time:.2f} seconds."
    )

# Allowed chars works as intended
if allowed_chars:
    print("+ Only allowed characters were found in a password when allowed_chars was provided.")
else:
    print(
        "- Either disallowed chars were found when allowed_chars was provided, "
        "or the parameter has not been implemented."
    )

# Ignored chars works as intended
if ignored_chars:
    print("+ No ignored characters were found in a password when ignored_chars was provided.")
else:
    print(
        "- Either ignored chars were found when ignored_chars was provided, "
        "or the parameter has not been implemented."
    )

# Summary
basics = (
    returns_string
    and correct_length
    and random_password
    and has_symbols
    and has_uppercase
)

advanced = (
    complete_time < 5.0
    and allowed_chars
    and ignored_chars
    and raises_user_warning
)

all_tests = (
    returns_string,
    correct_length,
    random_password,
    has_symbols,
    has_uppercase,
    complete_time < 5.0,
    allowed_chars,
    ignored_chars,
    raises_user_warning,
)

percentage = int(sum(all_tests) / (len(all_tests) / 100))
print(f"\n===  Your score is {percentage}%  === \n")

if basics:
    print("* You have completed all the basic requirements, and have successfully qualified for the code jam.")
else:
    print("* You have NOT completed all the basic requirements, and are not yet qualified for the code jam.")

if advanced:
    print("* You have completed all the bonus requirements, and will be considered an advanced user.")
else:
    print("* You have NOT completed all the bonus requirements.")
