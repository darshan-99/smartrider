from .models import Adminside, Cars, Area, City
from django import forms


class profileForm(forms.ModelForm):
    # password_confirmation = forms.CharField(
    #
    #     max_length=70,
    #     widget=forms.PasswordInput(),
    #     required=True,
    # ) aa extra field like 'confirm password' mate

    class Meta:
        model = Adminside
        YEARS = [x for x in range(1921, 2021)]
        fields = ['adminUname', 'adminFname', 'adminLname', 'adminPass', 'adminCno', 'adminEmail', 'adminDOB',
                  'adminGender', 'adminPic']
        widgets = {
            'adminUname': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'adminFname': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'adminLname': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'adminPass': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'adminCno': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'adminEmail': forms.EmailInput(attrs={'class': 'form-control form-control-user'}),
            'adminDOB': forms.SelectDateWidget(years=YEARS),
            'admiGender': forms.Select(attrs={'class': 'form-control form-control-user'}),
            'adminPic': forms.ClearableFileInput()
        }
        labels = {
            'adminUname': 'User Name',
            'adminFname': 'First Name',
            'adminLname': 'Last Name',
            'adminPass': 'Password',
            'adminCno': 'Contact number',
            'adminEmail': 'Email',
            'adminDOB': 'Date Of Birth',
            'adminGender': 'Gender',
            'adminPic': 'Profile Picture',
        }

    def clean_adminUname(self):
        adminUname = self.cleaned_data.get('adminUname')
        # if adminUname == "":
        #     raise forms.ValidationError("This field cannot be null")
        # uname_qs = Adminside.objects.filter(adminUname=adminUname)
        # if uname_qs.exists():
        #     raise forms.ValidationError("existed email")
        # for i in Adminside.objects.all().filter(~Q(adminID=1)): make it dynamic
        #     if i.adminUname == adminUname:
        #         raise forms.ValidationError('already exist')
        return adminUname


class AddCar(forms.ModelForm):
    class Meta:
        model = Cars

        fields = ['carName', 'carCompany', 'carType', 'carCapacity', 'carPic']
        widgets = {
            'carName': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'carCompany': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'carType': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'carCapacity': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'carPic': forms.ClearableFileInput()
        }
        labels = {
            'carName': 'Model Name',
            'carCompany': 'Car Company',
            'carType': 'Car Type',
            'carCapacity': 'Car Capacity',
            'carPic': 'Image',
        }


class UpdateCar(forms.ModelForm):
    class Meta:
        model = Cars

        fields = ['carName', 'carCompany', 'carType', 'carCapacity', 'carPic']
        widgets = {
            'carName': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'carCompany': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'carType': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'carCapacity': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'carPic': forms.ClearableFileInput()
        }
        labels = {
            'carName': 'Model Name',
            'carCompany': 'Car Company',
            'carType': 'Car Type',
            'carCapacity': 'Car Capacity',
            'carPic': 'Image',
        }


class AddArea(forms.ModelForm):
    class Meta:
        model = Area

        fields = ['areaName', 'pincode', 'cityID']
        widgets = {
            'areaName': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'city': forms.ModelChoiceField(queryset=City.objects.all(), initial=0)
        }
        labels = {
            'areaName': 'Area Name',
            'pincode': 'Pincode',
            'City Name': 'City Name',
        }


class UpdateArea(forms.ModelForm):
    class Meta:
        model = Area

        fields = ['areaName', 'pincode', 'cityID']
        widgets = {
            'areaName': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'city': forms.ModelChoiceField(queryset=City.objects.all(), initial=0)
        }
        labels = {
            'areaName': 'Area Name',
            'pincode': 'Pincode',
            'City Name': 'City Name',
        }


class AddCity(forms.ModelForm):
    class Meta:
        model = City

        fields = ['cityName']
        widgets = {
            'cityName': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }
        labels = {
            'cityName': 'City Name',
        }


class UpdateCity(forms.ModelForm):
    class Meta:
        model = City

        fields = ['cityName']
        widgets = {
            'cityName': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }
        labels = {
            'cityName': 'City Name',
        }
