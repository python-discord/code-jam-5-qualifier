
from timeit import timeit


print(timeit("""
import string
numbers = string.digits
lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
symbols = string.punctuation

ignored_chars = "123abcDABCEDF#$%"

if ignored_chars:
    # Create a new set object from a potentially exhaustible iterable, like an iterator
    ignored_chars = set(ignored_chars)

    numbers = list(set(numbers) - ignored_chars)
    lowercase = list(set(lowercase) - ignored_chars)
    uppercase = list(set(uppercase) - ignored_chars)
    symbols = list(set(symbols) - ignored_chars)
"""))
