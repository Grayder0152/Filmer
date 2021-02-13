from django.views.generic import CreateView
from django.conf import settings
from django.core.mail import send_mail
from .models import UsersEmail
from .forms import UsersEmailForm


class EmailView(CreateView):
    model = UsersEmail
    form_class = UsersEmailForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        address = request.POST.get('email')
        send_mail('Подписка на рассылку', 'Поздравляю, вы успешно подписались на рассылку', settings.EMAIL_HOST_USER,
                  [address])
        return super().post(request, *args, **kwargs)