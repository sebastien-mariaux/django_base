from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _


class HomeView(TemplateView):
    template_name = 'home.html'
    title = _('Home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context
