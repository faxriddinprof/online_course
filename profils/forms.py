from django import forms
from .models import Profile
from users.models import CustomUser  # 👈 email uchun kerak


class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # 👈 user.email ni olish

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'age', 'image', 'email']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email  # user.emailni forma ichida ko‘rsatamiz

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # user.email ham yangilansin
            if 'email' in self.cleaned_data:
                profile.user.email = self.cleaned_data['email']
                profile.user.save()
        return profile
