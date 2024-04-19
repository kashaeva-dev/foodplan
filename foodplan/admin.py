from django.contrib import admin
from django.utils.safestring import mark_safe

from foodplan.models import MealType, Allergy, Ingredient, MenuType, Recipe, RecipeIngredient, MealTypeRecipe, \
    MenuTypeRecipe, SubscriptionMealType, Subscription, SubscriptionAllergy, UserRecipe


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


class SubscriptionMealTypeInline(admin.TabularInline):
    model = SubscriptionMealType
    extra = 1


class SubscriptionAllergyInline(admin.TabularInline):
    model = SubscriptionAllergy
    extra = 1


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    inlines = (SubscriptionMealTypeInline,
               SubscriptionAllergyInline,
               )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline,
               MealTypeRecipeInline,
               MenuTypeRecipeInline,
               )
    list_display = ('name',
                    'total_calories_per_person_display',
                    'total_weight_per_person_display',
                    )

    def total_calories_per_person_display(self, obj):
        return int(obj.get_total_calories_per_person())
    total_calories_per_person_display.short_description = 'Калории на порцию'

    def total_weight_per_person_display(self, obj):
        return int(obj.get_total_weight_per_person())
    total_weight_per_person_display.short_description = 'Вес порции, г'


@admin.register(MenuType)
class MenuTypeAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'preview', 'description', ]
    readonly_fields = ['preview', ]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" style="max-height: 150px;">')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'protein', 'fat', 'carbohydrate', 'energy', 'allergy']
    list_editable = ['protein', 'fat', 'carbohydrate', 'energy', 'allergy']
    list_filter = ['allergy']
    search_fields = ['name']
    ordering = ['name']


admin.site.register(MealType)
admin.site.register(Allergy)
admin.site.register(UserRecipe)
admin.site.register(SubscriptionMealType)
admin.site.register(SubscriptionAllergy)
