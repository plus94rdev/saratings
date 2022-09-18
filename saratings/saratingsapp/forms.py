from django import forms
from .models import *
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible



# Create div for display errors
class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return mark_safe('<div class="invalid-feedback">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self]))



class EventRSVPForm(forms.ModelForm):
    
    confirm_attendance = forms.ChoiceField(
        choices=[('', 'Select...'), ('yes', 'Yes')], required=True)
    
    def __init__(self, *args, **kwargs):
        super(EventRSVPForm, self).__init__(*args, **kwargs)

        self.label_suffix = ""
        self.error_class = DivErrorList

        # Add class to format the input fields
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-group textinput textInputt form-control', }
            self.label_suffix = ""

    class Meta:
        model = EventRSVP
        fields = '__all__'

        

class RegulatoryArticleCommentForm(forms.ModelForm):
    
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)

    
    def __init__(self, *args, **kwargs):
        super(RegulatoryArticleCommentForm, self).__init__(*args, **kwargs)

        self.label_suffix = ""
        self.error_class = DivErrorList

        # Add class to format the input fields
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-group textinput textInputt form-control', }
            self.label_suffix = ""
            
        

    class Meta:
        model = RegulatoryArticleComment
        fields = '__all__'



