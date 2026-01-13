from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Count
from .models import Show, Country, Director, Actor, CountriesCast
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ShowForm


def index(request):
    active_tab = request.GET.get('tab', 'shows')
    page_number = request.GET.get('page', 1)
    
    context = {
        'active_tab': active_tab,
        'page_title': 'Netflix DB',
        'page_obj': None,
        'columns': [],
        'stats': None
    }

    if active_tab == 'shows':
        data = Show.objects.all().order_by('show_id')
        context['table_title'] = 'Фильмы и Сериалы'
        context['columns'] = ['ID', 'Название', 'Тип', 'Год', 'Рейтинг', 'Страны', 'Действия']
    
    elif active_tab == 'actors':
        data = Actor.objects.all().order_by('actor_name')
        context['table_title'] = 'Актеры'
        context['columns'] = ['ID', 'Имя']

    elif active_tab == 'directors':
        data = Director.objects.all().order_by('director_name')
        context['table_title'] = 'Режиссеры'
        context['columns'] = ['ID', 'Имя']
        
    elif active_tab == 'countries':
        data = Country.objects.all().order_by('country_name')
        context['table_title'] = 'Страны'
        context['columns'] = ['ID', 'Название']
        
    elif active_tab == 'stats':
        stats_data = (
            CountriesCast.objects
            .values('country__country_name')
            .annotate(total=Count('show'))
            .order_by('-total')[:20]
        )
        context['stats'] = stats_data
        context['table_title'] = 'Статистика: Топ-20 стран'
        data = []

    else:
        data = []

    if active_tab != 'stats':
        paginator = Paginator(data, 20)
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj

    return render(request, 'main/index.html', context)

def add_show(request):
    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            new_show = form.save()
            
            selected_countries = form.cleaned_data['countries']
            for country in selected_countries:
                CountriesCast.objects.create(show=new_show, country=country)
                
            return redirect('index')
    else:
        form = ShowForm()

    return render(request, 'main/show_form.html', {'form': form, 'title': 'Добавить новый фильм'})


def edit_show(request, pk):
    show = get_object_or_404(Show, pk=pk)
    
    if request.method == 'POST':
        form = ShowForm(request.POST, instance=show)
        if form.is_valid():
            form.save()
            
            CountriesCast.objects.filter(show=show).delete()
            
            selected_countries = form.cleaned_data['countries']
            for country in selected_countries:
                CountriesCast.objects.create(show=show, country=country)
                
            return redirect('index')
    else:
        existing_countries = Country.objects.filter(countriescast__show=show)
        form = ShowForm(instance=show, initial={'countries': existing_countries})

    return render(request, 'main/show_form.html', {'form': form, 'title': f'Редактировать: {show.title}'})


def delete_show(request, pk):
    show = get_object_or_404(Show, pk=pk)
    
    if request.method == 'POST':
        show.delete()
        return redirect('index')
        
    return render(request, 'main/delete_confirm.html', {'show': show})