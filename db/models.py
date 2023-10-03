from django.db import models

# Create your models here.


class Cofactor(models.Model):
    element = models.CharField(max_length=10, unique=True)
    charge = models.IntegerField()
    atomic_radius = models.FloatField()
    atomic_mass = models.FloatField()
    ionization_energy = models.FloatField()
    electron_affinity = models.FloatField()
    ionic_radii = models.FloatField()
    z = models.IntegerField()

    class Meta:
        pass

    def __str__(self):
        return self.element


class Condition(models.Model):
    temperature = models.IntegerField()
    c_dnazyme = models.FloatField('DNAZyme concentration')
    c_substrate = models.FloatField('Substrate concentration')
    pH = models.FloatField()
    hepes = models.FloatField(default=0)
    epps = models.FloatField(default=0)
    tris_hcl = models.FloatField(default=0)
    ches = models.FloatField(default=0)
    histidine = models.FloatField(default=0)
    na_po4 = models.FloatField('Na2HPO4/NaH2PO4', default=0)
    edta = models.FloatField(default=0)
    mes = models.FloatField(default=0)
    alcohol = models.FloatField(default=0)
    atrazine = models.FloatField(default=0)
    sodium_coc = models.FloatField('Sodium cacodylate', default=0)
    mops = models.FloatField(default=0)
    tween = models.FloatField('Tween-20', default=0)
    acetate = models.FloatField(default=0)
    ag_1 = models.FloatField('Ag+ ions concentraion', default=0)
    ca_2 = models.FloatField('Ca 2+ ions concentraion', default=0)
    cd_2 = models.FloatField('Cd 2+ ions concentraion', default=0)
    co_2 = models.FloatField('Co 2+ ions concentraion', default=0)
    mg_2 = models.FloatField('Mg 2+ ions concentraion', default=0)
    mn_2 = models.FloatField('Mn 2+ ions concentraion', default=0)
    ni_2 = models.FloatField('Ni 2+ ions concentraion', default=0)
    pb_2 = models.FloatField('Pb 2+ ions concentraion', default=0)
    sm_3 = models.FloatField('Sm 3+ ions concentraion', default=0)
    zn_2 = models.FloatField('Zn 2+ ions concentraion', default=0)

    class Meta:
        pass

    def __str__(self):
        pass


class Enzyme(models.Model):
    sequence = models.CharField(max_length=200)
    kobs = models.FloatField()