from datetime import timedelta

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
        'format': 'yyyy-mm-dd HH:ii P',
        'autoclose': 'true',
        #'showMeridian' : 'true'
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
							'format': 'yyyy-mm-dd HH:ii P',
							'autoclose': 'true',
							#'showMeridian' : 'true'
							}
		widgets = {
					'start_at': DateTimeWidget(options=dateTimeOptions),
					'finish_at': DateTimeWidget(options=dateTimeOptions),
					'user': forms.HiddenInput(),
					'task': forms.HiddenInput()
				  }


	def clean(self):
		start = self.cleaned_data.get('start_at')
		end = self.cleaned_data.get('finish_at')
		if start and end and end - start > timedelta(hours=8):
			raise forms.ValidationError("Tracking time limit is 8h")
		return self.cleaned_data


class UserWorkLogReportForm(forms.Form):
	user = forms.ModelChoiceField(
		required=True,
		queryset=User.objects.all() if User.objects.all().count() > 0 else User.objects.get_empty_query_set(),
		empty_label="--",
	)
	start_at = forms.CharField(required=True, widget=DateTimeWidget())
	finish_at = forms.CharField(required=True, widget=DateTimeWidget())


class ProjectReportForm(forms.Form):
	project = forms.ModelChoiceField(
       required=True,
       queryset=Project.objects.all() if Project.objects.all().count() > 0 else Project.objects.get_empty_query_set(),
       empty_label="--",
    )


class ExportForm(forms.Form):
	exp_file = forms.FileField(label='')#widget=forms.FileInput(attrs={'class': 'btn btn-info'}))