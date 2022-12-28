from django.shortcuts import redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from data_manager.models import Events
from django.views import View
import io, csv
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from .forms import CreateEventForm
from datetime import datetime
from datetime import date

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