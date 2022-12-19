from django.contrib.auth import forms as auth_forms, get_user_model


class UserCreateForm(auth_forms.UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name',
                  'last_name',
                  'username',
                  'password1',
                  'password2',)
