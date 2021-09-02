from .models import Profile
from django.contrib.auth.models import User


def userHRD(request):
    hrd = Profile.objects.get(user__username=request.user, is_hrd=True)
    if request.user == 'Anonymous':
        pass
    return {'hrd': hrd}
