from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from trackers_app.models import Tracking
from trackers_app.standings import standings
from .forms import EntryForm
from .calendars import elimination_calendar

# Create your views here.
@login_required
def home(request):
    trackings = request.user.trackings.filter(is_active=True)
    return render(request, "leaderboard/home.html", {"trackings": trackings})


@login_required
def detail(request, pk):
    tracking = get_object_or_404(request.user.trackings, pk=pk)
    rows = standings(tracking)
    ctx = {"tracking": tracking}
    if tracking.kind == Tracking.Kind.ELIMINATION:
        entries = tracking.entries.select_related("user")
        ctx.update(
            standing=[u for u in rows if u.out_at is None],
            out=[u for u in rows if u.out_at is not None],
            months=elimination_calendar(tracking, entries, request.user),
        )
    else:
        ctx.update(rows=rows, entries=tracking.entries.select_related("user")[:50])
    return render(request, "leaderboard/detail.html", ctx)


@login_required
def add_entry(request, pk):
    tracking = get_object_or_404(request.user.trackings, pk=pk, is_active=True)
    form = EntryForm(request.POST or None, tracking=tracking, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("leaderboard:detail", pk=tracking.pk)
    return render(request, "leaderboard/add_entry.html", {"tracking": tracking, "form": form})
