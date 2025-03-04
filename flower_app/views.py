from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Bouquet, Consultation, Client, Order, BouquetOrder, Reason, PriceCategory
from .forms import OrderForm, ConsultationForm
import random
from django.contrib.auth.decorators import user_passes_test


def index(request):
    flowers = Bouquet.objects.order_by('?')[:3]
    context = {
        'is_index_page': True,
        'flowers': flowers
    }

    return render(request, 'index.html', context)


def catalog_api(request):
    flower_list = Bouquet.objects.filter(assortment=True)
    reasons = Reason.objects.all()
    paginator = Paginator(flower_list, 6)

    page = request.GET.get('page')
    try:
        flowers = paginator.page(page)
    except PageNotAnInteger:
        flowers = paginator.page(1)
    except EmptyPage:
        flowers = paginator.page(paginator.num_pages)

    return render(
        request,
        template_name='catalog.html',
        context={
            'flowers': flowers,
            'reasons': reasons,
        }
    )


def catalog_sorted(request, reason):
    flower_list = Bouquet.objects.filter(assortment=True, reason__title=reason)
    paginator = Paginator(flower_list, 12)

    page = request.GET.get('page')
    try:
        flowers = paginator.page(page)
    except PageNotAnInteger:
        flowers = paginator.page(1)
    except EmptyPage:
        flowers = paginator.page(paginator.num_pages)

    return render(
        request,
        template_name='sorted_catalog.html',
        context={
            'flowers': flowers,
            'reason': reason
        }
    )


def card(request, id):
    flower = get_object_or_404(Bouquet, id=id)
    return render(
        request,
        template_name='card.html',
        context={
            'flower': flower
        }
    )


def order(request, id):
    flower = get_object_or_404(Bouquet, id=id)

    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['fname']
            phone = form.cleaned_data['tel']
            address = form.cleaned_data['adres']

            # Создаем запись клиента
            client, created = Client.objects.get_or_create(phone=phone, defaults={'name': name, 'address': address})

            # Создаем заказ
            order = form.save(commit=False)
            order.client = client
            order.delivery_time_slot = form.cleaned_data['orderTime']
            order.delivery_address = address
            client.name = name
            client.save()
            order.save()

            # Создаем заказ букета
            bouquet_order = BouquetOrder(bouquet=flower, order=order, quantity=1)
            bouquet_order.save()

            # Перенаправляем на страницу подтверждения или на другую страницу
            return redirect('order_result', id=order.id)

    else:
        form = OrderForm()

    context = {
        'form': form,
        'flower': flower,
    }

    return render(request, 'order.html', context)


def order_result(request, id):
    order = get_object_or_404(Order, id=id)
    bouquet_order = BouquetOrder.objects.get(order=order)
    flower = bouquet_order.bouquet
    return render(
        request,
        template_name='order_result.html',
        context={
            'order': order,
            'flower': flower,
        }
    )


def quiz(request):
    reasons = Reason.objects.all()
    context = {
        'reasons': reasons
    }
    return render(request, 'quiz.html', context)


def quiz_step(request, reason):
    price_categories = PriceCategory.objects.all()
    context = {
        'price_categories': price_categories,
        'reason': reason,
    }
    return render(request, 'quiz-step.html', context)


def quiz_result(request, reason, category):
    reason = Reason.objects.filter(title=reason).first()
    category = PriceCategory.objects.filter(title=category).first()
    bouquets = Bouquet.objects.get_price_category(category, reason)
    if bouquets:
        bouquet = random.choice(bouquets)
    else:
        bouquet = None
    context = {'bouquet': bouquet}
    return render(request, 'result.html', context)


def is_manager(user):
    return user.is_staff


def create_consultation(request):
    if request.method == "POST":
        form = ConsultationForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['fname']
            phone = form.cleaned_data['tel']
            consult, created = Consultation.objects.get_or_create(phone=phone, defaults={'name': name})

            consult.name = name
            consult.save()

    return render(request, 'index.html')


@user_passes_test(is_manager, login_url='admin:login')
def consultations(request):
    consults = get_list_or_404(Consultation.objects.order_by('-status'))

    return render(request, 'consults.html', {'consultations': consults})
