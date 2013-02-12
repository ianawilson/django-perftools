def contains(iterator, value):
    for k in iterator:
        if value.startswith(k):
            return True
    return False


def get_culprit(frames, modules=[]):
    best_guess = None
    for frame in frames:
        try:
            culprit = '.'.join([frame.f_globals['__name__'], frame.f_code.co_name])
        except:
            continue
        if contains(modules, culprit):
            if not best_guess:
                best_guess = culprit
        elif best_guess:
            break

    return best_guess

def get_cache_key(environ):
    prefix = 'django_profiling_' 
    key = prefix
    if 'REMOTE_ADDR' in environ:
        key += environ['REMOTE_ADDR']
    if 'REMOTE_HOST' in environ:
        key += environ['REMOTE_HOST']

    # if we weren't able to make a unique key, give up
    if key == prefix:
        return None
    return key
