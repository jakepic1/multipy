multipy
=======

Clojure-style multimethods in Python.

Python's class-based polymorphism allows for function implementation overloading based on the type of an argument. However, some other languages (like Clojure), allow for implementation overloading based on an arbitrary dispatch function. (See http://clojure.org/multimethods).


Example
-------
The following code will dispatch based on calling the ``len`` function on the argument. The ``Default`` value is used if the dispatcher can't find any other match, similar to Clojure's ``:default``.

```python
from multi import defmulti, method, Default

defmulti('get_size', len)

@method(1)
def get_size(obj):
    return 'Just one!'

@method(2)
def get_size(obj):
    return 'A couple items...'

@method(Default)
def get_size(obj):
    return 'Some unkown size.'

```

Then:

```python
>>> get_size([1])
'Just one!'

>>> get_size([1, 2])
'A couple items...'

>>> get_size([1, 2, 3])
'Some unkown size.'

```


Dispatching on multiple functions using ``juxt``
------------------------------------------------
It is also possible to switch implementations based on multiple dispatch functions by combining functions using ``juxt``.

```python
from multi import defmulti, method, Default, juxt

defmulti('get_size', juxt(type, len))

@method((dict, 1))
def get_size(obj):
    return 'Dict of 1 pair'

@method((dict, 2))
def get_size(obj):
    return 'Dict of 2 key-value pairs.'

@method((list, 1))
def get_size(obj):
    return 'Single-element list'

@method((list, 2))
def get_size(obj):
    return 'A list with 2 elements!'

```

Using it:

```python
>>> get_size([1])
'Single-element list'

>>> get_size([1, 2])
'A list with 2 elements!'

>>> get_size({"one": 1})
'Dict of 1 pair'

>>> get_size({"one": 1, "two": 2})
'Dict of 2 key-value pairs.'

```


Dispatching based on number of args
-----------------------------------
Since multipy is so general, dispatching on number of args is trivial.

```python
from multi import defmulti, method, arity

defmulti('farity', arity)

@method(1)
def farity(x):
    return x

@method(2)
def farity(x, y):
    return x, y

```



Dispatching on type and number of args
--------------------------------------
multipy has a ``types`` function for dispatching on types and arity of args, similar to Guido van Rossum's original implementation of multimethods (http://www.artima.com/weblogs/viewpost.jsp?thread=101605).

```python
from multi import defmulti, method, types, Default

defmulti('add', types)

@method((int,))
def add(x):
    return add(x, 0)

@method((int, int))
def add(x, y):
    return x + y

@method((list, list))
def add(xs, ys):
    return map(add, xs, ys)

@method(Default)
def add(*args):
    return reduce(add, args)

```
