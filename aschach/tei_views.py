from django.http import HttpResponse

from django.shortcuts import get_object_or_404

from . models import Angabe


def angabe_as_tei(request, pk):
    obj = get_object_or_404(Angabe, pk=pk)
    mytei = obj.as_tei()
    return HttpResponse(mytei, content_type="text/xml")
