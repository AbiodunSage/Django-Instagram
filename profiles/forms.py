from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    username=forms.CharField()
    bio=forms.CharField()
  

    class Meta:
        model=Profile
        fields=['username','bio','Image']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control'})
        self.fields['bio'].widget.attrs.update({'class':'form-control'})
        self.fields['Image'].widget.attrs.update({'class':'form-control'})

    def save(self,commit=True):
        user=self.instance.user
        user.username=self.cleaned_data['username']
        user.save()
        return super().save(commit=commit)