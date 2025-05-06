from django.db import models
from django.contrib.auth.models import User

class Mesaj(models.Model):
    baslik = models.CharField(max_length=100)
    icerik = models.TextField()
    tarih = models.DateTimeField(auto_now_add=True)
    yazar = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.baslik
    
    class Meta:
        verbose_name_plural = "Mesajlar"
        ordering = ['-tarih']  #yeni mesajlar en üstte