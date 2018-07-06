Title: Ad-hoc objects in Python
Date: July 6, 2018
Category: Python
Tags: python


If you know one programming language, it's natural to look for parallels as you learn a new language. In my case, I've coded in JavaScript for many years while Python is much more recent for me. I regularly find myself thinking "in JavaScript, I'd do ..."
 
Take object handling. I really like JavaScript's dynamic handling of objects. With JS, there's no need to create a class template (though you can). Just create an ad-hoc object and start assigning it properties and methods. For example:


    :::javascript
    // JavaScript example
    var js_obj = {};

    // dynamically add a property
    js_obj.foo = 'bar';

    // and use it
    console.log(js_obj.foo); // bar

    // you can even create methods
    js_obj.sum = function(x, y) {
        return x + y;
    }
    // and use them
    console.log(js_obj.sum(3, 4)); // 7

What wasn't obvious to me at first was that I could do similar things in Python. I saw the `class ClassName()` syntax and was fooled into thinking that I had to predefine my class with all its attributes and methods before I could instantiate objects from it. Not perfectly parallel, but in Python, we can do this:

    :::python
    # Python example
    class Object(object):
        pass


    py_obj = Object()
    py_obj.bar = 'baz'

    print(py_obj.bar)  # baz

    # we can dynamically assign methods with lambdas
    py_obj.sum = lambda x, y: x + y

    print(py_obj.sum(3, 4))  # 7


    # or even full functions
    def exponential(num):
        if num < 0:
            return 'undefined'
        exp = num
        start = num - 1
        for step_down in range(start, 0, -1):
            print(step_down)
            exp = exp * step_down
        return exp


    py_obj.exp = exponential

    print(py_obj.exp(5))  # 120

That's great. But a leg-up that JS has is that objects are "associative arrays" meaning that in addition to the dot-notation, we can use array notation (e.g. Python's dict notation) to access properties of JS objects:


    // this works in JS:
    js_obj['foo']

    # but in Python, this wouldn't work
    py_obj['bar']

Why would that matter you ask? If you need to dynamically access properties of an object, say by looping through a list of keys returned by an API, the associative array notation comes in very handy. 

Here I present a simple class that gives similar functionality in Python. The Object class will create an object that you can access with either dot or dict notation. It offers support for iteration via `items()` and could be used by methods expecting a `__getitem__` accessor. 

    #!python
    class Object(object):
        '''
        Creates an object for simple key/value storage; enables access via
        object or dictionary syntax (i.e. obj.foo or obj['foo']).
        '''

        def __init__(self, **kwargs):
            for arg in kwargs:
                setattr(self, arg, kwargs[arg])

        def __getitem__(self, prop):
            '''
            Enables dict-like access, ie. foo['bar']
            '''
            return self.__getattribute__(prop)

        def __str__(self):
            '''
            String-representation as newline-separated string useful in print()
            '''
            state = [f'{attr}: {val}' for (attr, val) in self.__dict__.items()]
            return '\n'.join(state)

        def items(self):
            '''
            Enables enumeration via foo.items()
            '''
            return self.__dict__.items()

To use it:

    :::python
    generic_object = Object(foo='bar')

    print(generic_object.foo)  # bar
    print(generic_object['foo'])  # bar

    // add attributes dynamically
    generic_object.baz = 123
    print(generic_object.baz)  # 123

    # iterate over its attributes
    for key, value in generic_object.items():
        print(key, value)

    # even use its convenience string representation
    print(generic_object)  # prints multi-line string of key/values


This simple generic object class uses a couple of the <a href="https://docs.python.org/3/reference/datamodel.html#special-method-names" target="_blank">special attribute names</a> common to all Python objects. By overriding `__getitem__`, `__str__`, and `items` we give custom functionality to objects created from this class.

Just because you can, doesn't mean you should. Many would argue that ad-hoc objects like this are not "Pythonic." There are other data structures in Python that can serve a similar purpose as generic containers of data:


* There's the Dict (dictionary) and for pre-Python 3.7, OrderedDict. The disadvantage to dicts is the way you access their attributes &mdash; `my_dict['some_attribute']`. It's wordy, and to me inelegant compared to the `my_object.some_attribute` syntax of objects.
* <a href="https://docs.python.org/3/library/collections.html#collections.namedtuple" target="_blank">Named tuples</a> offer similar functionality, though like "normal" tuples, they are immutable.
* And starting with Python 3.7, you have <a href="https://docs.python.org/3/library/dataclasses.html" target="_blank">data classes</a> (also see <a href="https://hackernoon.com/a-brief-tour-of-python-3-7-data-classes-22ee5e046517" target="_blank">Hackernoon's overview article</a>). If you can use Python 3.7, data classes are superior to my simple class above (such as enforcing type hinting) so use them instead.

As always, use the data structure that best suits your needs and will most clearly communicate to future readers of your code its purpose and requirements. But don't be afraid to explore the ins and outs of the language too.