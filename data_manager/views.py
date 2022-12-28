from django.shortcuts import redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from data_manager.models import Events
from django.views import View
import io, csv, json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .forms import CreateEventForm
from datetime import datetime, date
from django.views.decorators.csrf import csrf_exempt

class EventCreate(LoginRequiredMixin, CreateView):
    model = Events
    fields = "__all__"
    success_url ="/event"

    def post(self, request, *args, **kwargs):
        request.POST._mutable = True
        country = request.POST["country"]
        request.POST.update({"country": country.replace("-", " ")})
        return super().post(request, *args, **kwargs)


class EventUpdate(LoginRequiredMixin, UpdateView):
    model = Events
    fields = "__all__"
    success_url ="/event"

class EventDelete(LoginRequiredMixin, DeleteView):
    model = Events
    success_url ="/event"

class BulkEventCreate(View):
    def post(self, request, *args, **kwargs):
        paramFile = io.TextIOWrapper(request.FILES["bulkcreatfile"].file)
        portfolio1 = csv.DictReader(paramFile)
        list_of_dict = list(portfolio1)
        try:
            objs = [
                Events(
                    country=row["country"].replace("-", " "),
                    title=row["title"],
                    date=date(datetime.strptime("2018-04-02", "%Y-%m-%d").year,datetime.strptime("2018-04-02", "%Y-%m-%d").month, datetime.strptime("2018-04-02", "%Y-%m-%d").day),
                    notes=row["notes"],
                    bunting=True if row["bunting"] and  row["bunting"] == "true" else False,
                )
                for row in list_of_dict
            ]

        except Exception as e:
            messages.error(request, f"Invalid formate of csv!")
            messages.error(request, f"Error While Importing Data: {str(e)}")
            return redirect("/event")
        try:
            Events.objects.bulk_create(objs)
            messages.success(request, "Data added successfully.")
        except Exception as e:
            messages.error(request, f"Error While Importing Data: {str(e)}")
        return redirect("/event")

class InventoryListView(ListView):
    model = Events
    fields = "__all__"
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_form"] = CreateEventForm
        return context


class CalendarView(ListView):
    model = Events
    fields = "__all__"
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event_form"] = CreateEventForm
        return context

@csrf_exempt
def EditEvents(request):
    if request.method == "POST":
        event_bulk_update_list = []
        event_bulk_create_list = []

        for event_data in json.loads(request.body.decode('utf-8')):
            if event_data[0]:
                event_obj = Events.objects.get(id=event_data[0])
                event_obj.title = event_data[1]
                event_obj.country = event_data[2]
                event_obj.date = event_data[3]
                event_obj.notes = event_data[4]
                event_obj.bunting = event_data[5]

                event_bulk_update_list.append(event_obj)
            else:
                event_bulk_create_list.append(Events(title = event_data[1], country = event_data[2],
                                        date = date(datetime.strptime(event_data[3], "%Y-%m-%d %H:%M:%S").year,datetime.strptime(event_data[3], "%Y-%m-%d %H:%M:%S").month, datetime.strptime(event_data[3], "%Y-%m-%d %H:%M:%S").day),
                                        notes = event_data[4], bunting = event_data[5]))
                
        Events.objects.bulk_create(event_bulk_create_list)
        Events.objects.bulk_update(event_bulk_update_list, ['title','country', 'date', 'notes', 'bunting'])   
    return render(request, 'spreadsheet.html', {'events': Events.objects.all()})