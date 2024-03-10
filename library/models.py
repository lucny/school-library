from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Autor(models.Model):
    jmeno = models.CharField(max_length=100, verbose_name='Jméno', help_text='Zadejte jméno autora',
                             error_messages={'null': 'Zadejte jméno autora',
                                             'max_length': 'Maximální délka je 100 znaků',
                                             'blank': 'Jméno nesmí být prázdné'})
    prijmeni = models.CharField(max_length=100, verbose_name='Příjmení', help_text='Zadejte příjmení autora',
                                error_messages={'null': 'Zadejte příjmení autora',
                                                'max_length': 'Maximální délka je 100 znaků',
                                                'blank': 'Příjmení nesmí být prázdné'})
    narozeni = models.DateField(blank=True, null=True, verbose_name='Datum narození',
                                help_text='Zadejte datum narození autora')
    umrti = models.DateField(blank=True, null=True, verbose_name='Datum úmrtí',
                             help_text='Zadejte datum úmrtí autora')
    zivotopis = models.TextField(blank=True, null=True, verbose_name='Životopis')
    fotografie = models.ImageField(upload_to='autori/', blank=True, null=True, verbose_name='Fotografie autora')

    class Meta:
        ordering = ['prijmeni', 'jmeno']
        verbose_name = 'Autor'
        verbose_name_plural = 'Autoři'

    def __str__(self):
        return f'{self.jmeno[0]}. {self.prijmeni} ({self.narozeni.year}-{self.umrti.year if self.umrti else "dosud žije"})'


class Zanr(models.Model):
    nazev = models.CharField(max_length=20, verbose_name='Název žánru', help_text='Zadejte název žánru',
                             error_messages={'null': 'Zadejte název žánru',
                                             'max_length': 'Maximální délka je 20 znaků',
                                             'blank': 'Název nesmí být prázdný'})

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Žánr'
        verbose_name_plural = 'Žánry'

    def __str__(self):
        return self.nazev


class Vydavatelstvi(models.Model):
    nazev = models.CharField(max_length=100, verbose_name='Název vydavatelství',
                             help_text='Zadejte název vydavatelství',
                             error_messages={'null': 'Zadejte název vydavatelství',
                                             'max_length': 'Maximální délka je 100 znaků',
                                             'blank': 'Název nesmí být prázdný'})
    adresa = models.TextField(blank=True, null=True, verbose_name='Adresa vydavatelství')

    class Meta:
        ordering = ['nazev']
        verbose_name = 'Vydavatelství'
        verbose_name_plural = 'Vydavatelství'

    def __str__(self):
        return self.nazev


class Kniha(models.Model):
    titul = models.CharField(max_length=100, verbose_name='Titul', help_text='Zadejte titul knihy',
                             error_messages={'required': 'Titul je povinné pole',
                                             'max_length': 'Maximální délka je 100 znaků',
                                             'blank': 'Titul nesmí být prázdný'})
    obsah = models.TextField(blank=True, null=True, verbose_name='Obsah knihy')
    pocet_stran = models.PositiveIntegerField(blank=True, null=True, verbose_name='Počet stran',
                                              validators=[MaxValueValidator(9999)],
                                              error_messages={'max_value': 'Maximální počet stran je 9999'},
                                              help_text='Zadejte počet stran knihy (max. 9999)')
    rok_vydani = models.PositiveIntegerField(blank=True, null=True, verbose_name='Rok vydání',
                                             validators=[MinValueValidator(1500), MaxValueValidator(2100)],
                                             error_messages={'min_value': 'Minimální rok vydání je 1500',
                                                             'max_value': 'Maximální rok vydání je 2100'},
                                             help_text='Zadejte rok vydání knihy (1500 - 2100)')
    obalka = models.ImageField(upload_to='obalky/', blank=True, null=True, verbose_name='Obálka knihy')
    autor = models.ManyToManyField(Autor, verbose_name='Autor/autoři knihy', help_text='Vyberte autora/autory knihy',
                                   error_messages={'null': 'Vyberte autora/autory knihy',
                                                   'blank': 'Autor nesmí být prázdný'})
    zanr = models.ManyToManyField(Zanr, verbose_name='Žánr/žánry knihy', help_text='Vyberte žánr/žánry knihy',
                                  error_messages={'null': 'Vyberte žánr/žánry knihy',
                                                  'blank': 'Žánr nesmí být prázdný'})
    vydavatelstvi = models.ForeignKey(Vydavatelstvi, on_delete=models.RESTRICT, verbose_name='Vydavatelství',
                                      blank=True, null=True)

    class Meta:
        ordering = ['titul']
        verbose_name = 'Kniha'
        verbose_name_plural = 'Knihy'

    def __str__(self):
        return f'{self.titul} ({self.rok_vydani})'
