from django import forms

from nails_project.schedule.models import Schedule


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'is_required': True,
                },
            ),
            'start_time': forms.TimeInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'is_required': False,
                    'placeholder': 'Start Time for example 09:00',
                }
            ),
            'end_time': forms.TimeInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control',
                    'is_required': False,
                    'placeholder': 'End Time end for example 22:22',
                }
            ),
            'available': forms.NullBooleanSelect(
                attrs={
                    'class': "form-select"
                }
            )
        }

