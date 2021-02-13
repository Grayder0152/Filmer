from django import template
from contact.forms import UsersEmailForm

register = template.Library()


@register.inclusion_tag('contact/tags/form.html')
def email_form():
    return {'email_form': UsersEmailForm()}
