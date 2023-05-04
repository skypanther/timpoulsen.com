There are a few python tips/tricks here that could be put into one post or a series of posts.

# Enum enhancements

code below, plus cover the 3.11 Enum enhancements like StrEnum

```
from enum import Enum, EnumMeta


class TackleEnumMeta(EnumMeta):
    """
    Defines a new meta field for Enums that inherit from this class so that you can do
    `if "foo" in some_enum`. Note that when we update to Python 3.11, we can just use
    the built-in StrEnum class to get this functionality.
    """

    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True


class EnumValueAliases(Enum, metaclass=TackleEnumMeta):
    """
    Enable a single Enum member to represent multiple values. For example:

        ```
        class EnumWithAliases(EnumValueAliases):
            AWS = "AWS", "ACE"

        print(EnumWithAliases("ACE"))     # EnumWithAliases.AWS
        print(EnumWithAliases("AWS"))     # EnumWithAliases.AWS

        ```
    """

    def __new__(cls, value, *value_aliases):
        obj = object.__new__(cls)
        obj._value_ = value
        for alias in value_aliases:
            if alias not in cls:
                # add the alias only if the value doesn't already exist directly
                cls._value2member_map_[alias] = obj
        return obj
```

Maybe there's a way to use https://stackoverflow.com/a/66784416/292947 or https://stackoverflow.com/a/66725750/292947 to mimic inheriting from str when using the two bases above.

```
# so there's this:
class Foobar1(str, Enum):
    FOO = "bar"

# which lets you do something like
if "bar" == Foobar1.FOO:
    pass

# But, you can't do this:
class Foobar1(str, EnumValueAliases):
    FOO = "bar"
 
# and this breaks for other reasons
class Foobar1(EnumValueAliases, str):
    FOO = "bar"

```



# Get a Boolean value from any

Say you want to convert "True", "False", "true", etc. to a `bool` ... turns out it's a bit complicated

```
import ast
 
def get_bool_from_any(some_val):
    if type(some_val) is not str:
        return bool(some_val)
    try:
        # Use ast.literal_eval() rather than eval() to safely evaluate the input string
        # lowercase/capitalize to handle strings that aren't lead-capitalized
        value = ast.literal_eval(some_val.lower().capitalize())
    except ValueError:
        # String value isn't parseable by ast, so check for custom falsey strings
        return some_val.lower() not in ['no', 'none', 'null']
    except SyntaxError:
        # empty strings and multi-word strings will raise a syntax error
        return False
    return bool(value)

tf_values = ["Yes", "True", "", "true", "To be or not to be", "TRUE", True, "No", "False", "false", "FALSE", False, 1, 0, None, {}, {"a": False}]

for tf in tf_values:
    print(f"`{tf}` is {get_bool_from_any(tf)}")

```

# Splitting a camelCase or PascalCase string into a space-delimited string or list

```
RE_WORDS = re.compile(r'''
    # Find words in a string. Order matters!
    [A-Z]+(?=[A-Z][a-z]) |  # All upper case before a capitalized word
    [A-Z]?[a-z]+ |  # Capitalized words / all lower case
    [A-Z]+ |  # All upper case
    \d+  # Numbers
''', re.VERBOSE)

RE_WORDS.findall('FOOBar')  # returns a list, so join with ' '.join(the_list)

```
