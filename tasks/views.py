import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render

from .models import Tasks


def all_tasks(request):
    all_events = Tasks.objects.all()

    # if filters applied then get parameter and filter based on condition else return object
    if request.GET:  
        event_arr = []

        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['name'] = i.name
            start_date = datetime.datetime.strptime(str(i.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.datetime.strptime(str(i.end_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start_date'] = start_date
            event_sub_arr['end_date'] = end_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

    context = {
        "events": all_events,
    }
    return render(request, 'tasks/all_tasks.html', context)


# Add  to template

"""
<script>

    $(document).ready(function() {

        $('#calendar').fullCalendar({
            defaultDate: '2016-07-19',
            editable: true,
            eventLimit: true, // allow "more" link when too many events
            events: [
                {% for i in events %}
                {
                    title: "{{ i.event_name}}",
                    start: '{{ i.start_date|date:"Y-m-d" }}',
                    end: '{{ i.end_date|date:"Y-m-d" }}',

                },
                {% endfor %}

            ]
        });

    });

</script>
"""
