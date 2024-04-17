from django.db import models


class MealType(models.Model):
    name = models.CharField(max_length=40, verbose_name='Тип блюда')

    class Meta:
        verbose_name = 'Тип блюда'
        verbose_name_plural = 'Типы блюд'

    def __str__(self):
        return self.name


class Allergy(models.Model):
    name = models.CharField(max_length=40, verbose_name='Тип аллергии')

    class Meta:
        verbose_name = 'Тип аллергии'
        verbose_name_plural = 'Типы аллергии'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=40, verbose_name='Ингредиент')
    allergy = models.ForeignKey(Allergy,
                                on_delete=models.SET_NULL,
                                verbose_name='Аллергия',
                                related_name='ingredients',
                                null=True,
                                blank=True,
                                )
    caloricity = models.IntegerField(verbose_name='Калорийность, ккал')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class MenuType(models.Model):
    name = models.CharField(max_length=40, verbose_name='Диета')
    image = models.ImageField(verbose_name='Изображение', upload_to='diets')

    class Meta:
        verbose_name = 'Тип меню'
        verbose_name_plural = 'Типы меню'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=40, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(verbose_name='Изображение', upload_to='recipes')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='Ингредиенты',
                                         related_name='recipes',
                                         through='RecipeIngredient',
                                         )
    menu_type = models.ForeignKey(MenuType,
                                  on_delete=models.PROTECT,
                                  verbose_name='Тип меню',
                                  related_name='recipes',
                                  )
    meal_type = models.ForeignKey(MealType,
                                  on_delete=models.PROTECT,
                                  verbose_name='Тип блюда',
                                  related_name='recipes',
                                  )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def total_calories(self):
        return sum([ingredient.quantity * (ingredient.ingredient.caloricity / 100)
                    for ingredient in self.ingredients.all()])


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.PROTECT,
                               verbose_name='Рецепт',
                               related_name='recipe_ingredients',
                               )
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.PROTECT,
                                   verbose_name='Ингредиент',
                                   related_name='recipe_ingredients',
                                   )
    quantity = models.IntegerField(verbose_name='Количество, г')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.ingredient} - {self.quantity}'
