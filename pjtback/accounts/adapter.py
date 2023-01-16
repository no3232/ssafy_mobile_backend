from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.phone_number = data.get('phone_number')
        user.profile_image = data.get('profile_image')
        user.naver_email = data.get('naver_email')
        user.google_email = data.get('google_email')
        user.kakao_email = data.get('kakao_email')
        user.nickname = data.get('nickname')
        user.age = data.get('age')

        user.save()
        return user