from django import forms
from .models import User,UserProfile
from .validators import allow_only_image_validator

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password','confirm_password']
    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Password did not match")
    
# def allow_only_image_validator(value):
#         ext = os.path.splitext(value.name)[1] #value=image.jpg
#         print(ext)
#         valid_extention = ['.jpg','.png','.jpeg']
#         if not ext.lower() in valid_extention:
#             raise ValidationError("Unsupported file extention. Allowed extention" + str(valid_extention))

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter your address','required':'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image_validator])
    
    # METHOD 1: To make a latitude and longitude read only
    
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longitude']
        
    # METHOD 2: To make a latitude and longitude read only bt __init__
    
    def __init__(self,*args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
                