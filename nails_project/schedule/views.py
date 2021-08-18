from datetime import date

from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins
from nails_project.schedule.forms import ScheduleForm
from nails_project.schedule.models import Schedule


class ScheduleCreateView(auth_mixins.LoginRequiredMixin, generic.FormView):
    form_class = ScheduleForm
    template_name = 'schedule/schedule_create.html'

    def form_valid(self, form):
        schedule = form.save(commit=False)
        schedule.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        schedules = Schedule.objects.all().order_by('date', 'start_time')
        context['schedules'] = schedules
        return context

    def get_success_url(self):
        url = reverse_lazy('schedule create')
        return url

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ScheduleListView(generic.ListView):
    model = Schedule
    template_name = 'schedule/schedule_view.html'
    context_object_name = 'schedules'
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # schedules = Schedule.objects.all().order_by('date', 'start_time')
        monday = Schedule.objects.filter(date__week_day=2).order_by('date', 'start_time')
        tuesday = Schedule.objects.filter(date__week_day=3).order_by('date', 'start_time')
        wednesday = Schedule.objects.all().filter(date__week_day=4).order_by('date', 'start_time')
        thursday = Schedule.objects.all().filter(date__week_day=5).order_by('date', 'start_time')
        friday = Schedule.objects.all().filter(date__week_day=6).order_by('date', 'start_time')
        saturday = Schedule.objects.all().filter(date__week_day=7).order_by('date', 'start_time')
        sunday = Schedule.objects.all().filter(date__week_day=1).order_by('date', 'start_time')
        # context["schedules"] = schedules
        context['monday'] = monday
        context['tuesday'] = tuesday
        context['wednesday'] = wednesday
        context['thursday'] = thursday
        context['friday'] = friday
        context['saturday'] = saturday
        context['sunday'] = sunday
        today = date.today()
        current_month = self.months[today.month]
        context['current_month'] = current_month
        return context


class ScheduleDeleteView(auth_mixins.LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    template_name = 'schedule/schedule_delete.html'
    success_url = reverse_lazy('schedule create')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
