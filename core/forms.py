from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from .models import Server


class ArrayWidget(forms.SelectMultiple):
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        value = context['widget']['value']
        choices = list(zip(value, value))
        context['widget']['choices'] = choices
        context['widget']['optgroups'] = self.optgroups(name, value, attrs)
        return context

    def optgroups(self, name, value, attrs=None):
        """Return a list of optgroups for this widget."""
        groups = []
        has_selected = False

        base_choices = list(zip(value, value))
        for index, (option_value, option_label) in enumerate(base_choices):
            if option_value is None:
                option_value = ''

            subgroup = []
            if isinstance(option_label, (list, tuple)):
                group_name = option_value
                subindex = 0
                choices = option_label
            else:
                group_name = None
                subindex = None
                choices = [(option_value, option_label)]
            groups.append((group_name, subgroup, index))

            for subvalue, sublabel in choices:
                selected = (
                    str(subvalue) in value and
                    (not has_selected or self.allow_multiple_selected)
                )
                has_selected |= selected
                subgroup.append(self.create_option(
                    name, subvalue, sublabel, selected, index,
                    subindex=subindex, attrs=attrs,
                ))
                if subindex is not None:
                    subindex += 1
        return groups

    def format_value(self, value):
        """Return selected values as a list."""
        if value is None and self.allow_multiple_selected:
            return []
        if not isinstance(value, (tuple, list)):
            value = value.split(',')
        return [str(v) if v is not None else '' for v in value]


class ServerForm(forms.ModelForm):
    class Meta:
        model = Server
        fields = (
            "prefix",
            "roles",
            "streaming_role",
            "streaming_role_requires",
        )
        widgets = {
            # TODO: This should be a subclass that implements correct translation
            # to/from comma-delimited ArrayField format.
            "roles": ArrayWidget,
        }

    helper = FormHelper()
    helper.form_class = "form-horizontal"
    helper.label_class = 'col-lg-2'
    helper.field_class = 'col-lg-4'
    helper.add_input(Submit('submit', 'Update'))
