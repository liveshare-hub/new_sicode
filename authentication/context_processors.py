from .models import Profile
# from django.contrib.auth.models import User


def ProPic(request):
    # propic = Profile.objects.select_related(
    #     'user').get(user__username=request.user)
    if request.user.is_superuser:
        propic = None
        return {'propic': propic}

    elif request.user.is_authenticated:
        propic = Profile.objects.filter(
            user__username=request.user)
        if not propic.exists():
            propic = None
        else:
            propic = propic.first()
            return {'propic': propic}
    else:
        propic = None
        return {'propic': propic}
