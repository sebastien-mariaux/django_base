from django.conf import settings


def site_title(request):    # pylint: disable=unused-argument
    return {"SITE_TITLE": settings.SITE_TITLE}
