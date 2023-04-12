from aschach.models import Angabe
from django.db.models import Count


def angabe_by_date(by="year"):
    grouped = list(
        Angabe.objects.filter(datum__gt="1699-01-01")
        .values(f"datum__{by}")
        .annotate(total=Count(f"datum__{by}"))
        .order_by(f"datum__{by}")
    )
    items = [list(x.values()) for x in grouped]
    return items
