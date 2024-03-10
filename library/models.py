from django.db import models


# Create your models here.

class Autor(models.Model):
    jmeno = models.CharField(max_length=100)
    prijmeni = models.CharField(max_length=100)
    narozeni = models.DateField()
    umrti = models.DateField(blank=True, null=True)
    zivotopis = models.TextField()
    fotografie = models.ImageField(upload_to='autori/')

    def __str__(self):
        return f'{self.jmeno} {self.prijmeni}'


class Zanr(models.Model):
    nazev = models.CharField(max_length=100)

    def __str__(self):
        return self.nazev


class Vydavatelstvi(models.Model):
    nazev = models.CharField(max_length=100)
    adresa = models.TextField()

    def __str__(self):
        return self.nazev


class Kniha(models.Model):
    titul = models.CharField(max_length=100)
    obsah = models.TextField()
    pocet_stran = models.IntegerField()
    rok_vydani = models.IntegerField()
    autor = models.ManyToManyField(Autor)
    zanr = models.ManyToManyField(Zanr)
    vydavatelstvi = models.ForeignKey(Vydavatelstvi, on_delete=models.CASCADE)

    def __str__(self):
        return self.titul
