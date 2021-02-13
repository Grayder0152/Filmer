from django.db import models
from datetime import date
from django.urls import reverse


class Category(models.Model):
    """Категории"""
    name = models.CharField("Категории", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Актеры"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={'slug': self.name})

    class Meta:
        verbose_name = "Актеры и Режиссеры"
        verbose_name_plural = "Актеры и Режиссеры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанры"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Фильмы"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2019)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name="режиссеры",
                                       related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name="акстеры",
                                    related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name="жанры")
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="укажите сумму ы дорлларых")
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="укажите сумму ы дорлларых")
    fees_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="укажите сумму ы дорлларых")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={'slug': self.url})

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильмы"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадры из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звёзды рейтинга"""
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звёзды рейтинга"
        verbose_name_plural = "Звёзды рейтинга"
        ordering = ['-value']


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    stars = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звёзды")
    movie = models.ForeignKey(Movie, on_delete=models.CharField, verbose_name="фильми")

    def __str__(self):
        return f"{self.stars} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинги"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    """Комментарий"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=50000)
    parent = models.ForeignKey("self", verbose_name="Родитель",
                               on_delete=models.SET_NULL, blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзывы"
        verbose_name_plural = "Отзывы"



