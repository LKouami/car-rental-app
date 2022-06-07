from django import forms

from authentication.models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'type': 'password',
            'class': 'form-control',
            "id": "floatingInput",
            "placeholder": "Confirmer mot de passe"
        }
    ))
    
    class Meta:
        model = CustomUser
        fields = ["email","first_name", "last_name", "birth_date", "password"]
        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "floatingInput",
                    "placeholder": "Prénoms"
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    "type": "text",
                    "class": "form-control",
                    "id": "floatingInput",
                    "placeholder": "Nom"
                }
            ),
            
            'birth_date': forms.DateInput(
                attrs={
                    "type": "date",
                    "class": "form-control",
                    "id": "floatingInput",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "type": "email",
                    "class": "form-control",
                    "id": "floatingInput",
                    "placeholder": "E-mail"
                }
            ),

            'password': forms.PasswordInput(
                attrs={
                    "type": "password",
                    "class": "form-control",
                    "id": "floatingInput",
                    "placeholder": "Mot de passe"
                }
            )
        }
    
    def clean(self):
            cleaned_data = super(UserRegistrationForm, self).clean()
            email = cleaned_data.get('email')
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')

            if password and confirm_password:
                if password != confirm_password:
                    raise forms.ValidationError(
                        "Mot de passe non identique."
                    )
                elif len(password) < 8:
                    raise forms.ValidationError(
                        "Le mot de passe doit contenir au moins 8 caractères."
                    )
                elif CustomUser.objects.filter(email=email).exists():
                    raise forms.ValidationError(
                        "L'E-mail est déjà utilisé."
                    )

# class UserLoginForm(forms.ModelForm):

#     confirm_password = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             'type': 'password',
#             'class': 'form-control'
#         }
#     ))

#     current_password = forms.CharField(widget=forms.PasswordInput(
#         attrs={
#             'type': 'password',
#             'class': 'form-control'
#         }
#     ))

#     class Meta:
#         model = CustomUser
#         fields = ["email", "password", "first_name", "last_name"]

#         widgets = {
#             'email': forms.TextInput(
#                 attrs={
#                     "type": "email",
#                     "class": "form-control"
#                 }
#             ),

#             'first_name': forms.TextInput(
#                 attrs={
#                     "type": "text",
#                     "class": "form-control",
#                     "id": "floatingInput",
#                     "placeholder": "Prénoms"
#                 }
#             ),

#             'last_name': forms.TextInput(
#                 attrs={
#                     "type": "text",
#                     "class": "form-control",
#                     "id": "floatingInput",
#                     "placeholder": "Nom"
#                 }
#             ),

#             'password': forms.TextInput(
#                 attrs={
#                     "type": "password",
#                     "class": "form-control"
#                 }
#             )
#         }
