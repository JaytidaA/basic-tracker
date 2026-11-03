from django import forms
from trackers_app.models import Entry, Tracking


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["value", "details"]

    def __init__(self, *args, tracking, user, **kwargs):
        super().__init__(*args, **kwargs)
        # Set before validation: Entry.clean() reads these, and ModelForm
        # runs clean() during is_valid().
        self.instance.tracking = tracking
        self.instance.user = user
        if tracking.kind == Tracking.Kind.ELIMINATION:
            del self.fields["value"]   # model default of 1 applies
