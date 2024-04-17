from django.contrib import admin
from django.utils.safestring import mark_safe

from foodplan.models import MealType, Allergy, Ingredient, MenuType, Recipe, RecipeIngredient


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,)


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'preview', ]
    readonly_fields = ['preview', ]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 150px;">')


admin.site.register(MealType)
admin.site.register(Allergy)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
