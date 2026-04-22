from django.db import models

# Create your models here.
class Banner(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="banners/", null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title if self.title else "Banner {}".format(self.id)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Banner"
        verbose_name_plural = "Banners"