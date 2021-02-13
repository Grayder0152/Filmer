from django.db import models


class UsersEmail(models.Model):
    """Электронные адреса пользователей"""
    email = models.EmailField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Электронные адреса"
        verbose_name_plural = "Электронные адреса"
