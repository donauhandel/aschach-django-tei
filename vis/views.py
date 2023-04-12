from django.http import JsonResponse
from django.views.generic.base import TemplateView

from vis.utils import angabe_by_date


def angabe_by_date_view(request, by="year"):
    data = angabe_by_date(by=by)
    return JsonResponse(data, safe=False)


class VisOverviewView(TemplateView):
    template_name = "vis/overview.html"


class AngabeOverTimeView(TemplateView):
    template_name = "vis/angabe_over_time.html"

    def get_context_data(self, **kwargs):
        by = kwargs['by']
        context = super().get_context_data(**kwargs)
        context["by"] = by
        return context
