from django.contrib import admin
from django.utils.safestring import mark_safe

from foodplan.models import MealType, Allergy, Ingredient, MenuType, Recipe, RecipeIngredient, MealTypeRecipe, \
    MenuTypeRecipe


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    raw_id_fields = ['ingredient', ]


class MealTypeRecipeInline(admin.TabularInline):
    model = MealTypeRecipe
    extra = 1


class MenuTypeRecipeInline(admin.TabularInline):
    model = MenuTypeRecipe
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,
               MealTypeRecipeInline,
               MenuTypeRecipeInline,
               )


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'preview', ]
    readonly_fields = ['preview', ]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 150px;">')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'protein', 'fat', 'carbohydrate', 'energy', 'allergy']
    list_filter = ['allergy']
    search_fields = ['name']
    ordering = ['name']


admin.site.register(MealType)
admin.site.register(Allergy)
