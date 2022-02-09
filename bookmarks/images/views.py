from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from commom.decorators import ajax_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from .models import Image
from .forms import ImageCreateForm

# Create your views here.
@login_required
def image_create(request):
    """
    Usamos o decorador de função para evitar o acesso de usuarios não atenticados
    esperamos o metodo GET para cria uma instancia do formulario, verificamos se o 
    formulario é valido, usamos o cleaned_date para limpar o form e criamos uma nova
    instacia sem salvar o no bd, associamos o usuario atual a imagem e salvamos no bd
    """
    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)

    return render(request,
                  'images/image/create.html',
                  {'section': 'images',
                   'form': form})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request,
                  'images/image/detail.html',
                  {'section': 'images',
                   'image': image})


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:   
                image.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


@login_required
def image_list(request):
    """
    Recupera todas as imagens do db e constroi um objeto paginator, recuperando
    8 imagens por pagina, Se a pagina entiver fora do intervalo levanta EmptyPage
    por fim renderiza o resultado em dois templates. 
    """
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # Se a pagina não for um numero inteiro, mostra a primeira pagina
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # Se a solicitação for AJAX e a página estiver fora do intervalo
            # Retorna uma página vazia
            return HttpResponse('')
        # Se a página não estiver no intervalo mostra a ultima pagina
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/image/list_ajax.html',
                    {'section': 'images', 'images': images})
    return render(request, 'images/image/list.html',
                    {'section': 'images', 'images':images})