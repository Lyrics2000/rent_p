from django import forms

class SignINForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "name":"emailaddress", "type":"email" , "placeholder":"Email", "id":"username",
             "required":""

        }
    ))

    password = forms.CharField(
        widget=forms.PasswordInput(
           attrs={ "type":"password" ,"placeholder":"Password", "id":"password",
            "required":""}
        )
    )

    


class SignUpForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "name":"emailaddress", "type":"text" , "placeholder":"Username", "id":"username",
             "required":""

        }
    ))

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "name":"emailaddress", "type":"text" , "placeholder":"First Name", "id":"username",
             "required":""

        }
    ))

    last_name = forms.CharField(widget=forms.TextInput(
        attrs={
            "name":"emailaddress", "type":"text" , "placeholder":"Last Name", "id":"username",
             "required":""

        }
    ))

    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            "name":"phone", "type":"text" , "placeholder":"Phone Number", "id":"phone",
             "required":""

        }
    ))

    type = forms.CharField(widget=forms.TextInput(
        attrs={
            "name":"type", "type":"text" , "placeholder":"Type ...", "id":"type",
             "required":""

        }
    ))

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "name":"emailaddress", "type":"email" , "placeholder":"Username", "id":"email",
             "required":""

        }
    ))

    password = forms.CharField(
        widget=forms.PasswordInput(
           attrs={ "type":"password" ,"placeholder":"Password", "id":"password",
            "required":""}
        )
    )
