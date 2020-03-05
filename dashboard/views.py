from django.shortcuts import render
from django.views.generic.base import TemplateView

from organisations.models import AskingOrg


# Create your views here.
class Dashboard(TemplateView):

    template_name = "dashboard/index.html"
    redirect_field_name = None

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)

        context['orgs'] = AskingOrg.objects.all()

        return context
