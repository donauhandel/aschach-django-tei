from django.http import JsonResponse
from aschach.vis_utils import angabe_by_date


def angabe_by_date_view(request, by="year"):
    data = angabe_by_date(by=by)
    return JsonResponse(data, safe=False)
