import os
import markdown
from django.conf import settings
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _

README = os.path.join(settings.BASE_DIR, 'readme.md')


class HomeView(TemplateView):
    template_name = 'home.html'
    title = _('Home')

    @staticmethod
    def markdown_content():
        with open(README, 'r') as f:
            text = f.read()
            return markdown.markdown(text)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        context['readme'] = self.markdown_content()
        return context
