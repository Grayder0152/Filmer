from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('id', 'name', 'url')  # отображаются только эти поля
    list_display_links = ('name',)  # это поле является ссылкой на таблицу


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0  # дополнительные поля для нового коментария
    readonly_fields = ('name', 'email', 'text', 'parent')  # нельзя редактировать эти поля


class MovieShotInline(admin.TabularInline):
    model = MovieShots
    extra = 0
    list_display = ('image',)
    readonly_fields = ('title', 'description', 'image', 'movie', 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80">')

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('title', 'draft')  # список фильтрируется по данным полям
    search_fields = ('title', 'category__name')  # поиск реализуется по даным полям
    inlines = [MovieShotInline, ReviewInline]  # указаная модель этого класса отображается после содержимого обьекта
    save_on_top = True  # меню располагается сверху, а не снизу
    save_as = True  # возможность дублирование полей
    list_editable = ('draft',)  # поле можно редактировать прямо со списка
    readonly_fields = ('get_image',)
    form = MovieAdminForm  # стилизация форм описания
    actions = ['publish', 'unpublish']  # действие

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100">')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была добавлена'
        else:
            message_bit = f'{row_update} записей было обновлено'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была добавлена'
        else:
            message_bit = f'{row_update} записей было обновл'
        self.message_user(request, f'{message_bit}')

    get_image.short_description = "Постер"
    publish.short_description = 'Опубликовать'
    publish.allowed_permission = ('change',)
    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permission = ('change',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ('name', 'url')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('id', 'name', 'email', 'parent', 'movie')
    list_display_links = ('movie',)
    list_filter = ('id',)
    readonly_fields = ('name', 'email', 'text')


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ('id', 'name', 'age', 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100">')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ('ip', 'stars', 'movie')


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    """Звёзды рейтинга"""
    list_display = ('id', 'value')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ('id', 'title', 'movie', 'get_image')

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100">')

    get_image.short_description = "Изображение"


admin.site.site_title = 'Filmer'
admin.site.site_header = 'Filmer'
