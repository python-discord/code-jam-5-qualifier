# Our solution to the Code Jam Qualifier

This is our example solution to the qualifier assignment of Code Jam 5. It's a straightfoward implementation of the requirements and it doesn't aim to be the fastest, best, or most secure solution. In fact, we've seen a lot of interesting, alternative approaches during our review of the entries that are certainly not worse than ours.

## The solution

You can find the solution itself in the file `solution.py`. For a more in-depth explanation of how the code works and why we've made certain design choices, see the annotated parts of the solution below.

If you have questions about our solution, feel free to mention Ves Zappa in one of the off topic channels on the Python Discord server.

### The function signature
```py
from typing import Iterable, Optional


def generate_password(
    password_length: int = 8,
    has_symbols: bool = False,
    has_uppercase: bool = False,
    ignored_chars: Optional[Iterable[str]] = None,
    allowed_chars: Optional[Iterable[str]] = None
) -> str:
```

As you can see, we've type hinted the `ingored_chars` and `allowed_chars` parameters as `Optional[Interable[str]]`. While the qualifier itself states that "The user can provide a list in either of these parameters", we actually only need the provided arguments to be *iterable* (and finite in size) and chose to let the type hints reflect that. That's why imported the names `Iterable` and `Optional` from the `typing` module instead of type hinting the parameters as `List[str]`.

### A word on UserWarning
```py
    if ignored_chars and allowed_chars:
        raise UserWarning("`ignored_chars` and `allowed_chars` cannot be set at the same time")
```

We realized after publishing the qualifier that the `UserWarning` exception should actually be used with the `warning.warn` system in the standard library. However, since the qualifier clearly states that we should raise it, we did that here manually. Another approach would have been to change the warning level of the `warning.warn` functionality, but it was not really our intention to include the `warning` system in the qualifier. (Note: it's obviously fine if you did choose to use the `warning.warn` method.)

### The minimum password length
```py
    minimum_length = max(1, has_uppercase + has_symbols)
    if minimum_length > password_length:
        raise UserWarning(
            f"`password_length` must be at least {minimum_length} for the specified options."
        )
```

To be able to generate any password at all, we will need at least 1 character. However, when both a symbol and an uppercase letter are required, we need at least a length of two. That's why we determine the minimum password length here by using the built-in function `max`. Since it's always good to provide your user with feedback when something fails, we decided to include the minimum length for the specified options in the exception message.

### Local names for the character classes
```py
    numbers = string.digits
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    symbols = string.punctuation
```

Assigning local names for the four default characters classes we're using to generate the password allows us to potentially reassign those names later when we correct (some) of the character classes for `ignored_chars` or `allowed_chars`. This means that further down in the code, we can assume the character classes were assigned these names regardless of `ignored_chars` or `allowed_chars`.

### Sets and list comprehensions
```py
    if ignored_chars:
        # Create a new set object from a potentially exhaustible iterable, like an iterator
        ignored_chars = set(ignored_chars)

        numbers = [char for char in numbers if char not in ignored_chars]
        lowercase = [char for char in lowercase if char not in ignored_chars]
        uppercase = [char for char in uppercase if char not in ignored_chars]
        symbols = [char for char in symbols if char not in ignored_chars]
```

The first and foremost reason of creating a `set` out of the `ignored_chars` here is because membership tests (i.e, the `not in` tests) with `set` objects are really fast because they make use of hashtables. However, there are two other reasons for constructing a new object from the argument:

1. Some iterables in Python, like iterators, will yield elements until they are exhausted. At that point, they are done and you can't iterate over them again. As we need to do a lot of membership tests here, we first construct an iterable that can be iterated over multiple times.
2. The object passed as the argument `ignored_chars` could be *mutable*. If that happens, all changes we make to `ignored_chars` within the function will also be reflected to the original object outside of the function; this is called mutable aliasing. While this is not a problem in this version of the code, since we don't modify `ignored_chars` anywhere, it's generally a good idea to avoid mutable aliasing by constructing a new object from the argument provided to the function. The reason is that mutable aliasing can lead to bugs that are difficult to track down, since the change may pop-up in a totally different part of the code. [This Ned Batchelder video](https://www.youtube.com/watch?v=_AEJHKGk9ns) explains why this happens very well.

You may be wondering why we did not construct sets from all of the character classes and used `set methods` to filter out the `ignored_chars`. The reason is simple: Constructing a hashtable is relatively expensive and since we're not going to use the individual `set` objects more than once, just using a list comprehension is more efficient (Ves: about 30% faster on my machine). However, keep in mind that this code will run only once, if it runs at all, so efficiency isn't really important.

### random.choice and a subscriptable object
```py
    if allowed_chars:
        allowed_chars = set(allowed_chars)

        symbols = [char for char in symbols if char in allowed_chars]
        uppercase = [char for char in uppercase if char in allowed_chars]

        pool = list(allowed_chars)
    else:
        # We need a subscriptable object for `random.choices`
        pool = list(itertools.chain(lowercase, uppercase, numbers, symbols))

    password = random.choices(pool, k=password_length)
 ```

Since we want to use `random.choices` to generate a password of a certain length, we need to make sure that our character pool is subscriptable: The individual elements must be accessible by an integer index. This is why we need to construct a `list` object from the `allowed_chars` after we are done with the membership tests. This is still faster than using a `list` object for the `in` membership tests.

If we're not working with `allowed_chars`, we need to make a combined subscriptable object from the four default character classes. We do this by using `itertools.chain` to *chains* the four iterable character classes together and making a single list of all those "chained" elements.

Now that we have our final subscriptable character pool, we can use `random.choices` to quickly select a random password of the required length. This is much faster than picking the characters one-by-one in a loop using `random.choice`.


### Indices for a symbol and an uppercase
```py
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
```

However, we cannot use the password generated above as-is when `has_symbol` and or `has_uppercase` was specified, since drawing random characters doesn't guarantee that either of them is included in the password. To make sure the password contains the required characters, we select random positions in the password and replace the characters that were there by either a symbol or an uppercase letter.

First, we start by drawing the number of indices we need. We determine this by summing the boolean values `has_uppercase` and `has_sumbols`. Since `False` has a numeric value of `0` and `True` has a numeric value of `1`, this will give us the number of indices we need. By using `random.sample` instead of `random.choices`, we guarantee that the two indices will be different so we don't overwrite the just inserted symbol by the uppercase.

Now we've selected the indices for the symbol and the uppercase letter, we pick one randomly and the position in the list to it.

### Returning the password
```py
    return "".join(password)
```

Before this line, the password is still a `list` of characters. Since the returned password needs to be a `str` object, we simply join those characters together and return it.
