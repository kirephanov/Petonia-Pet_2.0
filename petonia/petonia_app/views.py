from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.core.paginator import Paginator
from django.http import HttpResponse
from .models import *
from .forms import MarkerForm, UserRegisterForm, UserLoginForm
from django.contrib import messages
from django.db.models import F
import folium
from geopy import MapBox
from  django.contrib.auth import login, logout

def login_page(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }

    return render(request=request, template_name='petonia_app/login.html', context=context)

def logout_page(request):
    logout(request)
    return redirect('login')

def register_page(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации.')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
    }
    return render(request=request, template_name='petonia_app/register.html', context=context)

def index(request):
    return render(request=request, template_name='petonia_app/index.html')

def map_page(request):
    marker = Marker.objects.all()
    context = {
        'marker': marker,
               }

    map = folium.Map(location=[55.558741, 37.378847], zoom_start=4)
    for item in marker:
        street = item.street
        city = item.city
        country = item.country
        place = '{0}, {1}, {2}'.format(street, city, country)

        comm_str = '''
        Имя: {0}      
        Категория: {1}     
        Питомец: {2} 
        Телефон: {3}
        Доп. инф.: {4}
        Место: {5}
        '''.format(item.name, item.search, item.animal, item.telephone, item.comment, place)

        location = MapBox(
            api_key='pk.eyJ1Ijoia29yaXRzZWUiLCJhIjoiY2t0NHE1cXFqMDEzcjJ3bjlpa3p0cXJxYiJ9.1rfq6OgGcgEfhE2H6dRWQQ').geocode(
            place)

        folium.Marker(location=[location.latitude, location.longitude], popup=comm_str, icon=folium.Icon(color='darkblue')).add_to(map)

    map.save('petonia_app/templates/petonia_app/map.html')
    return render(request=request, template_name='petonia_app/map.html', context=context)

def form_page(request):
    error = ''
    if request.method == 'POST':
        form = MarkerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            error = 'Форма была неверной.'

    form = MarkerForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request=request, template_name='petonia_app/form.html', context=data)

def bulletin_page(request):
    marker = Marker.objects.all()
    animals = Animal.objects.all()
    regions = Region.objects.all()
    categories = Search.objects.all()

    paginator = Paginator(marker, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)

    context = {'marker': marker, 'animals': animals, 'regions': regions, 'categories': categories, 'page_obj': page_obj}
    return render(request=request, template_name='petonia_app/board.html', context=context)

def get_region(request, region_id):
    marker = Marker.objects.filter(region_id=region_id)
    animals = Animal.objects.all()
    region = Region.objects.get(pk=region_id)
    regions = Region.objects.all()
    categories = Search.objects.all()

    paginator = Paginator(marker, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'marker': marker, 'animals': animals, 'region': region, 'regions': regions, 'categories': categories, 'page_obj': page_obj}
    return render(request, template_name='petonia_app/region.html', context=context)

def get_category(request, category_id):
    marker = Marker.objects.filter(search_id=category_id)
    animals = Animal.objects.all()
    regions = Region.objects.all()
    categories = Search.objects.all()
    category = Search.objects.get(pk=category_id)

    paginator = Paginator(marker, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'marker': marker, 'animals': animals, 'regions': regions, 'categories': categories, 'category': category, 'page_obj': page_obj}
    return render(request, template_name='petonia_app/category.html', context=context)

def get_animal(request, animal_id):
    marker = Marker.objects.filter(animal_id=animal_id)
    animals = Animal.objects.all()
    animal = Animal.objects.get(pk=animal_id)
    regions = Region.objects.all()
    categories = Search.objects.all()

    paginator = Paginator(marker, 10)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {'marker': marker, 'animals': animals, 'animal': animal, 'regions': regions, 'categories': categories, 'page_obj': page_obj}
    return render(request, template_name='petonia_app/animal.html', context=context)

class GetPost(DetailView):
    model = Marker
    template_name = 'petonia_app/single.html'
    context_object_name = 'marker'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context

def get_popular(request, cnt=10):
    marker = Marker.objects.order_by('-views')[:cnt]
    animals = Animal.objects.all()
    regions = Region.objects.all()
    categories = Search.objects.all()
    context = {'marker': marker, 'animals': animals, 'regions': regions, 'categories': categories}
    return render(request, template_name='petonia_app/popular.html', context=context)

def mobileLogin_page(request):
    return render(request=request, template_name='petonia_app/login-mobile.html')

def mobileLogout_page(request):
    return render(request=request, template_name='petonia_app/logout-mobile.html')