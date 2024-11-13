import calendar

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from appointments.models import Appointment
from diary.utils import get_next_month, get_month_first_last_dates

class DiaryView(LoginRequiredMixin, View):

    template_name = 'diary/diary.html'

    def get(self, request):

        today = timezone.now()
        today_num = today.day

        current_page_month_param = request.GET.get('currentMonth', None)
        move_direction_param = request.GET.get('move', None)

        changed_year = False

        if current_page_month_param and move_direction_param:
            month_num, changed_year = get_next_month(int(current_page_month_param), move_direction_param)
            month_str = calendar.month_name[month_num]
        else:
            month_num = today.month
            month_str = calendar.month_name[month_num]
        
        year = today.year

        if changed_year:
            if move_direction_param == 'left':
                year -= 1
            elif move_direction_param == 'right':
                year += 1

        month_first_date, month_last_date = get_month_first_last_dates(year, month_num)            

        month_calendar = calendar.monthcalendar(year, month_num)

        user = request.user
        user_appointments = Appointment.objects.filter(
            user=user,
            appointment_date__gte=month_first_date,
            appointment_date__lte=month_last_date
        )

        appointments_calendar = []

        for week_index, week in enumerate(month_calendar):

            week_data = []

            for day_index, day in enumerate(week):

                is_weekend = day_index in [5, 6]

                if day == 0:
                    week_data.append({"day": 0, "appointments": []})
                else:
                    day_appointments = [appt for appt in user_appointments if appt.appointment_date.day == day]
                    week_data.append({
                        "day": day,
                        "appointments": day_appointments,
                        "is_weekend": is_weekend,
                    })

            appointments_calendar.append(week_data)

        context = {
            'today_num': today_num,
            'month_str': month_str,
            'month_num': month_num,
            'month_today': today.month,
            'year': year,
            'year_today': today.year,
            'appointments_calendar': appointments_calendar,
        }

        return render(request, self.template_name, context)
    