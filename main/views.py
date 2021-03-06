from django.shortcuts import redirect, HttpResponse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Movie, Actor, Genre, Rating, RatingStar
from .forms import ReviewForm, RatingForm



class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values('year')


class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = "movies/movies.html"


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"  # поле по которому производится поиск
    template_name = "movies/movie_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['star_form'] = RatingForm()
        return context


class AddReview(View):
    """Отзыв"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = 'name'


class AddStarRating(View):
    """Добавление рейтнга фильму"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        Rating.objects.update_or_create(
            ip=self.get_client_ip(request),
            stars=RatingStar.objects.get(value=int(request.POST.get('star'))),
            movie=Movie.objects.get(title=request.POST.get('movie'))
        )
        return HttpResponse(status=201)


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""
    template_name = "movies/movies.html"

    def get_queryset(self):
        queryset = Movie.objects.filter(Q(year__in=list(map(int, self.request.GET.getlist('year')))) |
                                        Q(genres__in=self.request.GET.getlist('genre')))
        return queryset


class Search(ListView):
    """Поиск фильмов"""

    paginate_by = 3
    template_name = "movies/movies.html"

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = self.request.GET.get('q')
        return context



