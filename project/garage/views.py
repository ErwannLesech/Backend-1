from django.shortcuts import render

from django.http import HttpResponse

from django.template import loader

from django.shortcuts import get_object_or_404, render

from django.urls import reverse
from django.views import generic

from .models import motorcycle, detail

from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'garage/index.html'
    context_object_name = 'latest_motorcycle_list'

    def get_queryset(self):
        """Return the last five published motorcycles."""
        return motorcycle.objects.filter(pub_date__lte=timezone.now())


class DetailView(generic.DetailView):
    model = motorcycle
    template_name = 'garage/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return motorcycle.objects.filter(pub_date__lte=timezone.now())

def detail(request, motorcycle_id):
    motorcycle = get_object_or_404(motorcycle, pk=motorcycle_id)
    return render(request, 'motorcycle/detail.html', {'motorcycle': motorcycle})

def index(request):
    latest_motorcycle_list = motorcycle.objects.order_by('-pub_date')[:5]
    context = {'latest_motorcycle_list': latest_motorcycle_list}
    return render(request, 'motorcycle/index.html', context)

