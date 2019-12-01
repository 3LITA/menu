from django.db import models


class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False)
    menu_name = models.CharField(max_length=64, null=False)
    content = models.CharField(max_length=128, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children', blank=True)
