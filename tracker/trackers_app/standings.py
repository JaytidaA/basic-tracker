from django.db.models import Min, Sum, Q
from django.db.models.functions import Coalesce
from .models import Tracking

def standings(tracking):
    mine = Q(entries__tracking=tracking)

    if tracking.kind == Tracking.Kind.SUM:
        return list(
            tracking.members
            .annotate(score=Coalesce(Sum("entries__value", filter=mine), 0))
            .order_by("-score", "username")
        )

    # ELIMINATION: survivors first, then the eliminated, latest elimination ranked highest
    users = list(tracking.members.annotate(out_at=Min("entries__occurred_at", filter=mine)))
    survivors = sorted((u for u in users if u.out_at is None), key=lambda u: u.username)
    out = sorted((u for u in users if u.out_at), key=lambda u: u.out_at, reverse=True)
    return survivors + out
