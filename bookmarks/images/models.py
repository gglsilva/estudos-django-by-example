from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    """
    Armazena as imagens de diferentes sites
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)  # indica o usuario que marcou a imagem
    title = models.CharField(max_length=200)    # indica o titulo da imagem
    slug = models.SlugField(max_length=200,     # rotulo curto para a url da imagem
                            blank=True)
    url = models.URLField()     # indica a url da imagem
    image = models.ImageField(upload_to='images/%Y/%m/%d/')     # indica o arquivo da imagem
    description = models.TextField(blank=True)      # indica a descricao da imagem
    created = models.DateField(auto_now_add=True, # indica a data de criacao da imagem
                               db_index=True)
    users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                        related_name='images_liked',
                                        blank=True)     # indica os usuarios que curtiram a imagem

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])