_methods = {}


class Default(object):
    """
    Used to specify the default dispatch value for a multimethod.

    @method(Default)
    def something(*args):
        # This will run if the dispatch value doesn't match any other methods.
        ...

    """
    pass


class MultiMethod(object):
    def __init__(self, name, dispatch_fn):
        self.name = name
        self.dispatch_fn = dispatch_fn
        self._registry = {}

    def register(self, value, f):
        self._registry[value] = f

    def __call__(self, *args):
        """Calls the dispatch_fn """
        dispatch_val = self.dispatch_fn(*args)
        f_to_call = self._registry.get(dispatch_val, None)
        if f_to_call is None:
            try:
                f_to_call = self._registry[Default]
            except KeyError:
                raise NotImplementedError(
                    'No method found for "%s" with arguments %s' % (self.name, args))
        return f_to_call(*args)


def defmulti(name, dispatch_fn):
    """Registers the dispatch function with name."""
    _methods[name] = MultiMethod(name, dispatch_fn)

def method(value):
    """
    Decorator to register a new method that will be called when the
    dispatch function returns the matching value.

    """
    def fwrapper(f):
        try:
            mm = _methods[f.__name__]
        except KeyError:
            raise NameError('No multimethod "%s" found.' % f.__name__)
        mm.register(value, f)
        return mm
    return fwrapper

def juxt(*fs):
    """
    Takes a set of functions and returns a function that is the juxtaposition
    of those functions.  The returned function takes a variable number of args, and
    returns a tuple containing the result of applying each function to the
    args (left-to-right).
    juxt(a, b, c)(x) => (a(x), b(x), c(x),)

    """
    def juxted(*args):
        return tuple([f(*args) for f in fs])
    return juxted
