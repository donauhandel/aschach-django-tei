from django.http import JsonResponse
from django.urls import reverse
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
        context = super().get_context_data(**kwargs)
        by = kwargs["by"]
        if by not in ["day", "month", "year"]:
            by = "year"
        context["data_url"] = reverse("vis:angabe_by_date", kwargs={"by": by})
        context["unit"] = "Jahr"
        context["title"] = f"Mautprotokolleinträge pro {context['unit']}"
        if by == "month":
            context["unit"] = "Monat"
            context["title"] = f"Mautprotokolleinträge pro {context['unit']}"
        elif by == "day":
            context["unit"] = "Tag im Monat"
            context["title"] = "Mautprotokolleinträge pro Tag im Monat"
        context["by"] = by
        print(context["data_url"])
        return context
