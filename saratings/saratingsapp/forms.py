from django import forms
from django.forms.utils import ErrorList
from django.utils.safestring import mark_safe
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from saratingsapp.models import *


# Create div for display errors
class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ''
        return mark_safe('<div class="invalid-feedback">%s</div>' % ''.join(['<div class="error">%s</div>' % e for e in self]))


#


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("User does not exist")

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")

            if not user.is_active:
                raise forms.ValidationError("This user is not active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):

        # first call parent's constructor
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        # self.fields['first_name'].required = True
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-group textinput textInput form-control',}
            self.fields[field].label = ''
    class Meta:
        model = User
        fields = ['username','email','password1', 'password2']



class UserProfileForm(forms.ModelForm):
        
    email = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-group textinput textInput form-control',} 
            self.fields[field].label = ''

        # self.label_suffix = ""
        # self.error_class = DivErrorList

    class Meta:
        model = UserProfile
        fields = ['email','first_name','last_name','cell_number']


class UserProfileUpdateForm(forms.ModelForm):
        
    cell_number = forms.CharField(label='Cell Number', required=True,max_length=11)
    
    def __init__(self, *args, **kwargs):
        super(UserProfileUpdateForm, self).__init__(*args, **kwargs)

        self.label_suffix = ""
        self.error_class = DivErrorList

        # Add class to format the input fields
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-group textinput textInputt form-control', }
            self.label_suffix = ""

    class Meta:
        model = UserProfile
        fields = ['first_name','last_name','cell_number', 'email']


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



class NuggetCommentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(NuggetCommentForm, self).__init__(*args, **kwargs)

        self.label_suffix = ""
        self.error_class = DivErrorList

        # Add class to format the input fields
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-group textinput textInputt form-control', }
            self.label_suffix = ""
            
        

    class Meta:
        model = NuggetComment
        fields = ['comment']
        
        

class ResearchPurchaseForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ResearchPurchaseForm, self).__init__(*args, **kwargs)

        self.label_suffix = ""
        self.error_class = DivErrorList

        # Add class to format the input fields
        for field in self.fields:
            self.fields[field].widget.attrs = {
                'class': 'form-group textinput textInputt form-control', }
            self.label_suffix = ""
            
        
    class Meta:
        model = ResearchPurchase
        fields = '__all__'