from django import forms

from datetimewidget.widgets import DateTimeWidget

from timetrack.models import Project, Request, WorkLog, Task
from accounts.models import User



class FilterForm(forms.Form):
    start_date = forms.DateTimeField(required=False)
    end_date = forms.DateTimeField(required=False)
    project = forms.ModelChoiceField(
       required=False,
       queryset=Project.objects.all() if Project.objects.all().count() > 0 else Project.objects.get_empty_query_set(),
       empty_label="Any project",
    )
    min_estimate = forms.IntegerField(min_value=0, required=False)
    max_estimate = forms.IntegerField(min_value=0, max_value=99999, required=False)


class RequestForm(forms.ModelForm):

	class Meta:
		model = Request
		fields = ('request_type', 'description', 'start_at', 'finish_at', 'user',)
		dateTimeOptions = {
        'format': 'dd/mm/yyyy HH:ii P',
        'autoclose': 'true',
        'showMeridian' : 'true'
        }
		widgets = {
                	'start_at': DateTimeWidget(options=dateTimeOptions),
                	'finish_at': DateTimeWidget(options=dateTimeOptions),
                	'user': forms.HiddenInput()
            	  }


class WorkLogForm(forms.ModelForm):

	class Meta:
		model = WorkLog
		fields = ('work_type', 'start_at', 'finish_at', 'user', 'task')
		dateTimeOptions = {
							'format': 'dd/mm/yyyy HH:ii P',
							'autoclose': 'true',
							'showMeridian' : 'true'
							}
		widgets = {
					'start_at': DateTimeWidget(options=dateTimeOptions),
					'finish_at': DateTimeWidget(options=dateTimeOptions),
					'user': forms.HiddenInput(),
					'task': forms.HiddenInput()
				  }
