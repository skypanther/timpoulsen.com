Title: Getting a Boolean from any value in Python
Description: Python code to convert any data value into a Boolean in a human-intuitive way.
Date: 2023-07-14
Category: Python
Tags: python
Slug: python-bool-from-any

# Getting a Boolean value from any data type

Recently, I was building a webhook that needed to accept and operate on varied data from outside sources. Included in that data were values meant to be Booleans. However, some callers were sending values like `"Yes"` or `"no"` or even `"-1"`. I needed to convert each of those to a Boolean value based on their semantic meaning. In other words, we humans know that the string "false" should represent a `False` value. But on it's own, Python would treat the non-empty string as a `True` value.

I'll give background and explanation below. But for the impatient readers out there, here's the code I came up with.

    #!python
    import ast
    from numbers import Real
    from typing import Any

    def get_bool_from_any(val: Any) -> bool:
        # CC0 license https://creativecommons.org/publicdomain/zero/1.0/
        try:
            # First, try treating the input as a number so that we can
            # handle values such as 0, 1, -1, 0.1, etc.
            return float(val) > 0
        except:
            # Converting to a float failed, so, let's see if it's a string
            if type(val) is str:
                try:
                    # Use ast.literal_eval() rather than eval() to safely evaluate the input string
                    # lowercase/capitalize to handle strings that aren't lead-capitalized
                    # This statement will handle strings like True, true, False, FALSE, etc.
                    return ast.literal_eval(val.lower().capitalize())
                except ValueError:
                    # String value isn't parseable by ast, so check for custom falsey strings
                    return val.lower() not in ['no', 'none', 'null']
                except SyntaxError:
                    # empty strings and multi-word strings will raise a syntax error, treat that as False
                    return False
            else:
                # Finally, it's not a number or string so rely on Python's built-in coercion rules
                return bool(val)

In the actual project, I added a suite of tests around this function. For simplicity in this post, let's just manually check some values.

    :::python
    truthy_values = [True, "True", "true", "TRUE", "Yes", 1, "1", 0.1, {"a": False}]
    falsey_values = [False, "False", "false", "FALSE", "No", False, "To be or not to be", 0, "0", -1, None, {}]

    for val in truthy_values:
        print(f"`{val}` is {get_bool_from_any(val)}")

    for val in falsey_values:
        print(f"`{val}` is {get_bool_from_any(val)}")

## Changing data types

To understand what's going on in that function, we need to consider data types. Python is not a strongly-typed language like C or Java. However, the language does define data types, and generally requires you to operate on one type at a time. For example, you can't add an integer and a list.

When data types don't match, the Python interpreter will do its best to convert values so they do match. However, its rules for this _coercion_ don't always match what you might expect.

Originally, Python did not have a Boolean data type. One was added in [PEP 285](https://peps.python.org/pep-0285/) (way back in 2002!). In Python, `bool` inherits from `int` in order to maintain compatibility with code that was written before this type was added. This is why `1 == True` evaluates to be a true statement. It also means you can add `1 + True` to get `2`. Weird.

## Coercion rules in Python

That PEP and its implementation defined how the interpreter will coerce values into Booleans, which is summarized in this table.

| Input value                            | Coerced to |
| -------------------------------------- | ---------- |
| An empty string                        | `False`    |
| The string `"False"`                   | `False`    |
| Any other non-empty string             | `True`     |
| The number `0` or `0.0`                | `False`    |
| Any other number, positive or negative | `True`     |
| An empty list, object, or set          | `False`    |
| A list, object, or set with members    | `True`     |

For most situations, those rules are great. However, you'd probably expect `bool("false")` to return `False` when in fact it returns `True`. Lots of situations treat `-1` as a falsey value. And silly humans use strings like "Yes", "No", and so forth to represent Boolean-like values. We can do better!

## Digging into get_bool_from_any()

We finally have the background we need to understand the `get_bool_from_any()` function above. The `try` block that starts on line 7 handles numbers, as well as strings that can be converted to numbers like "0.1". For my purposes, it made sense that any value greater than 0 would be `True` and the rest `False`.

The `float(val)` call will raise an exception if `val` can't be converted to a number. So the next thing the function handles is strings. As the comment says, I use `ast.literal_eval()` rather than plain `eval()` since it's less vulnerable to injection attacks. (This function comes from the `ast` or Abstract Syntax Tree built-in library.) To handle upper- and lowercase variations, I convert to lowercase, then lead-capitalize the string. In this way, `"false"` will be parsed and converted to `False` as we'd expect.

The `ast.literal_eval()` function will raise an exception in a couple of cases. If it can't parse the word &mdash; in other words, it's not "False" or "True" &mdash; I catch the `ValueError` and test to see if the string is in my short list of falsey words. If so, the function returns `False` otherwise it returns `True`.

The other `except` block takes care of empty strings and multi-word strings. On its own, `ast.literal_eval()` raises a `SyntaxError` in those situations. I just treat those cases as falsey values and return `False`.

Finally, I handle input values that are something other than a string or number. Line 27 uses Python's `bool()` function to explicitly convert the input value to a Boolean. Following the rules described in the table above, this handles cases like empty or populated lists, objects, and so forth.

## Conclusion

I really didn't need a function that was this comprehensive. The callback payloads I was handling always contained strings, and the values were always one of a short list of variations. I mean, my function could have been as simple as:

    :::python
    def is_it_true(val):
        return val in ["true", "True", "yes", "Yes", "1"]

But, where's the fun in that? With my function, I handle just about any data type as an input value. I handle human-intuitive values like `-1` being a falsey value. And, I got to explore some library functions I would rarely use otherwise. Figuring out the logic of the if-else and try-except blocks gave my brain a little exercise too.

I hope you find the function useful, or you at least learned something from this post. If you find an error or an edge case, hit me up on Mastodon or put in a PR on this blog's repo; links are in the sidebar.
