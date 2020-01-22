from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from djangoql.admin import DjangoQLSearchMixin
from django.core import serializers

# Register your models here.
from .models import *
# from django.db.models import Count


class CustomModelAdmin(DjangoQLSearchMixin, ImportExportModelAdmin):
    def __init__(self, model, admin_site):
        self.list_display = [
            field.name for field in model._meta.fields if field.name != "id"]
        self.search_fields = [
            field.name for field in model._meta.fields if field.name != "id"]
        super(CustomModelAdmin, self).__init__(model, admin_site)


@admin.register(Gene)
class GeneAdmin(CustomModelAdmin):
    pass


@admin.register(Snp)
class SnpAdmin(CustomModelAdmin):
    pass


@admin.register(Trait)
class TraitAdmin(CustomModelAdmin):
    pass


@admin.register(Disease)
class DiseaseAdmin(CustomModelAdmin):
    pass


@admin.register(TraitSnp)
class TraitSnpAdmin(CustomModelAdmin):
    pass


@admin.register(DiseaseSnp)
class DiseaseSnpAdmin(CustomModelAdmin):
    pass


@admin.register(Paper)
class PaperAdmin(CustomModelAdmin):
    pass
