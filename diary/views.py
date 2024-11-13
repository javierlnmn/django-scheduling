import calendar
from datetime import datetime

from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

from appointments.models import Appointment
from diary.utils import get_next_prev_month, get_month_first_last_dates

class DiaryView(LoginRequiredMixin, View):

    template_name = 'diary/diary.html'

    def get(self, request):

        today = timezone.now()
        today_num = today.day

        month_param = request.GET.get('month', None)
        year_param = request.GET.get('year', None)

        if month_param and year_param:
            month_num = int(month_param)
            month_str = calendar.month_name[month_num]
            year = int(year_param)
        else:
            month_num = today.month
            month_str = calendar.month_name[month_num]
            year = today.year

        month_next, year_next_changed = get_next_prev_month(month_num, 'next')
        month_prev, year_prev_changed = get_next_prev_month(month_num, 'prev')
        year_next = year + 1 if year_next_changed else year
        year_prev = year - 1 if year_prev_changed else year

        month_first_date, month_last_date = get_month_first_last_dates(year, month_num)            

        month_calendar = calendar.monthcalendar(year, month_num)

        user = request.user
        user_appointments = Appointment.objects.filter(
            user=user,
            appointment_date__gte=month_first_date,
            appointment_date__lte=month_last_date
        ).order_by(
            'appointment_date',
            'appointment_time'
        )

        appointments_calendar = []

        for week_index, week in enumerate(month_calendar):

            week_data = []

            for day_index, day in enumerate(week):

                is_weekend = day_index in [5, 6]

                if day == 0:
                    week_data.append({"day": 0, "appointments": []})
                else:
                    week_day_date = datetime.strptime(f'{year}-{month_num}-{day}', '%Y-%m-%d').date()
                    day_appointments = user_appointments.filter(appointment_date=week_day_date)

                    day_passed = week_day_date < today.date()

                    week_data.append({
                        "day": day,
                        "appointments": day_appointments,
                        "is_weekend": is_weekend,
                        "day_passed": day_passed,
                    })

            appointments_calendar.append(week_data)

        context = {
            'today_num': today_num,
            'month_str': month_str,
            'month_num': month_num,
            'month_today': today.month,
            'month_next': month_next,
            'month_prev': month_prev,
            'year': year,
            'year_today': today.year,
            'year_next': year_next,
            'year_prev': year_prev,
            'appointments_calendar': appointments_calendar,
        }

        return render(request, self.template_name, context)
    