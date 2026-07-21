from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from dashboard.forms import ConversionChoiceForm, ConversionLengthForm, ConversionMassForm
from dashboard.services.conversion import convert_measurement


@login_required
def conversion(request):
    choice_form = ConversionChoiceForm(request.POST or None)
    measurement_form = None
    answer = None

    if request.method == "POST" and choice_form.is_valid():
        measurement = choice_form.cleaned_data["measurement"]
        form_class = ConversionLengthForm if measurement == "length" else ConversionMassForm
        is_conversion_submit = "value" in request.POST
        measurement_form = form_class(request.POST if is_conversion_submit else None)

        if is_conversion_submit and measurement_form.is_valid():
            value = measurement_form.cleaned_data["value"]
            from_unit = measurement_form.cleaned_data["from_unit"]
            to_unit = measurement_form.cleaned_data["to_unit"]
            answer = convert_measurement(value, from_unit, to_unit)

    return render(
        request,
        "dashboard/conversion.html",
        {
            "form": choice_form,
            "measurement_form": measurement_form,
            "answer": answer,
        },
    )
