import os
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from researchhub.settings import BASE_DIR
from utils.http import RequestMethods


def index(request):
    return HttpResponse("Authenticate with a token in the Authorization header.")


def permissions(request):
    path = os.path.join(BASE_DIR, "static", "researchhub", "user_permissions.json")
    with open(path, "r") as file:
        data = file.read()
    return HttpResponse(content=data, content_type="application/json")


@api_view([RequestMethods.GET])
@permission_classes(())
def healthcheck(request):
    """
    Health check for elastic beanstalk
    """

    return Response({"PONG"})


def robots_txt(request):
    content = render_to_string("robots.txt")
    return HttpResponse(content, content_type="text/plain")
