from urllib import request
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify
from .models import Image


class ImageCreateForm(forms.ModelForm):
    """
    Formulário para criar uma nova imagem, construido a partir do modelo Image
    o url e passado como parametro
    """
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }


    def clean_url(self):
        """
        Definimos o metodo cleaned_data para obter o campo url e
        Verifica se a extensão da imagem é valida(jpg, jpeg)
        se não for, retorna um erro.
        """
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg']
        extension = url.rsplit('.', 1)[1].lower()
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not ' \
                                        'match valid image extensions.')
        return url

    def save(self, force_insert=False,
                   force_update=False,
                   commit=True):
        """
        Substituiremos o metodo salve padrão do formulário para 
        recuperar a imagem fornecida e salva-la no banco de dados
        """
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        # download image from the given URL
        response = request.urlopen(image_url)
        image.image.save(image_name,
                         ContentFile(response.read()),
                         save=False)
        if commit:
            image.save()
        return image