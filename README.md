# Code Jam 5 Qualifier
For this code jam, we have provided you with the signature and docstring for a password generator function, and you must write the function body.

**The function must fulfill the following criteria to qualify you for the Code Jam:**
* Must return a string.
* Must generate a random password.
* The password must be exactly `password_length` characters long.
* If `has_symbols` is True, the password must contain at least one symbol, such as `#`, `!`, or `@`.
* If `has_uppercase` is True, the password must contain at least one uppercase letter.

**The following criteria are optional, but will net you extra points:**
* The generator should support `password_length` < 1 000 000 characters.
* The generator should not take more than 5 seconds to finish.
* Update the function signature to take two more optional parameters, `ignored_chars` and `allowed_chars`. 
  - The user can provide a list in either of these parameters to control which characters will be used to build the password.
  - Do not allow both lists to be passed at the same time. If this happens, raise a UserWarning explaining that only one may be passed.
  - Any characters in `ignored_chars` are guaranteed not to be used in the password.
  - Only characters in `allowed_chars` will be used in the password, if the list is present.
  - Update the docstring to explain how to use these new parameters.
  
## Automated testing
There are two files provided in this qualifier. 
* `qualifier.py` contains the actual task, and this is where you will write all of your code.
* `tests.py` contains tests that will verify whether or not you've completed the qualifier, and whether you've completed all the bonus criteria. You will need to run this file and copy-paste its output into the Code Jam Signup after you've written your code. It might also be helpful to run this in order to see how you're doing, especially if working through the bonus criteria. Please don't modify this file.

First finish writing all the code you need to solve this problem in `qualifier.py`, and then run `tests.py` from the same folder. We will need you to copy the output that `tests.py` generates as well as all the code you wrote in `qualifier.py` into your code jam application.


