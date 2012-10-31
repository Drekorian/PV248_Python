# processing states for the main process queue

class state(object):
    def __init__(self, value = None):
        self.value = value

class done(state):
    pass

class next(state):
    pass

class replace(state):
    pass

def is_done(o):
    return isinstance(o, done)

def is_next(o):
    return isinstance(o, next)

def is_replace(o):
    return isinstance(o, replace)
