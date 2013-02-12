from datetime import timedelta

from django.shortcuts import render
from django.core.cache import cache
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from .utils import get_cache_key
from .forms import ProfilingForm

@login_required
def profiling(request):
    current_time = now()
    status = ''
    
    if request.method == 'POST':
        form = ProfilingForm(request.POST)
        
        if form.is_valid():
            profiling_on = form.cleaned_data['profiling_on']
            
            # save profiling
            
            # turn on profiling
            if form.cleaned_data['profiling_on']:
                expires_in = form.cleaned_data['expiration'] - current_time
                cache.set(form.cleaned_data['cache_key'], form.cleaned_data['expiration'], expires_in.seconds)
                status = 'Enabled profiling for `%s` until %s' % (form.cleaned_data['cache_key'], form.cleaned_data['expiration'])
            # turn off profiling
            else:
                cache.delete(form.cleaned_data['cache_key'])
                status = 'Disabled profiling for `%s`' % (form.cleaned_data['cache_key'])
    # GET
    else:
        cache_key = get_cache_key(request.META)
        expiration = cache.get(cache_key)
        
        # if we don't have a stored expiration, we'll suggest one; profiling is off
        if not expiration:
            expiration = current_time + timedelta(minutes=5)
            profiling_on = False
            status = 'Profiling is not enabled for `%s`' % (cache_key)
        # if we did, profiling is turned on, so let them know that's true
        else:
            status = 'Profiling is on for `%s` until %s' % (cache_key, expiration)
            profiling_on = True
        
        initial = {
            'cache_key': cache_key,
            'expiration': expiration,
            'profiling_on': profiling_on,
        }
        
        form = ProfilingForm(initial=initial)
    
    return render(request, 'profiling.html', {'form': form, 'status': status, 'profiling_on': profiling_on})
