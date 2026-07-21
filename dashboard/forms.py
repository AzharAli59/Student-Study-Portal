from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Homework, Note, Todo


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                continue
            css_class = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{css_class} form-control".strip()
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = field.label or name.replace("_", " ").title()


class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class StyledAuthenticationForm(BootstrapFormMixin, AuthenticationForm):
    pass


class NoteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class HomeworkForm(BootstrapFormMixin, forms.ModelForm):
    due_at = forms.DateTimeField(
        required=False,
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
    )

    class Meta:
        model = Homework
        fields = ["subject", "title", "description", "due_at"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class TodoForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Todo
        fields = ["title"]


class SearchForm(BootstrapFormMixin, forms.Form):
    text = forms.CharField(
        label="Search",
        max_length=128,
        widget=forms.TextInput(attrs={"placeholder": "Enter a search term"}),
    )


class ConversionChoiceForm(forms.Form):
    MEASUREMENT_CHOICES = [
        ("length", "Length"),
        ("mass", "Mass"),
    ]

    measurement = forms.ChoiceField(
        choices=MEASUREMENT_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "portal-radio-list"}),
    )


class ConversionLengthForm(BootstrapFormMixin, forms.Form):
    UNIT_CHOICES = [
        ("yard", "Yard"),
        ("foot", "Foot"),
    ]

    value = forms.FloatField(min_value=0, label="", widget=forms.NumberInput(attrs={"placeholder": "Enter value"}))
    from_unit = forms.ChoiceField(label="", choices=UNIT_CHOICES)
    to_unit = forms.ChoiceField(label="", choices=UNIT_CHOICES)


class ConversionMassForm(BootstrapFormMixin, forms.Form):
    UNIT_CHOICES = [
        ("pound", "Pound"),
        ("kilogram", "Kilogram"),
    ]

    value = forms.FloatField(min_value=0, label="", widget=forms.NumberInput(attrs={"placeholder": "Enter value"}))
    from_unit = forms.ChoiceField(label="", choices=UNIT_CHOICES)
    to_unit = forms.ChoiceField(label="", choices=UNIT_CHOICES)
