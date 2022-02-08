from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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