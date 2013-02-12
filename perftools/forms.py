from django import forms

class ProfilingForm(forms.Form):
    cache_key = forms.CharField(help_text='Probably, you should not change this.')
    profiling_on = forms.BooleanField(required=False)
    expiration = forms.DateTimeField(help_text="Default is 5 minutes. I can't really recommend that you set this very far in the future.")
