from django.db import models
from django.conf import settings


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
    protein = models.FloatField(verbose_name='Белки, г', default=0)
    fat = models.FloatField(verbose_name='Жиры, г', default=0)
    carbohydrate = models.FloatField(verbose_name='Углеводы, г', default=0)
    energy = models.IntegerField(verbose_name='Калорийность, ккал')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class MenuType(models.Model):
    name = models.CharField(max_length=40, verbose_name='Тип меню')
    image = models.ImageField(verbose_name='Изображение', upload_to='diets')
    description = models.TextField(verbose_name='Описание', blank=True)

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
    menu_type = models.ManyToManyField(MenuType,
                                  verbose_name='Тип меню',
                                  related_name='recipes',
                                       through='MenuTypeRecipe',
                                  )
    meal_type = models.ManyToManyField(MealType,
                                  verbose_name='Тип блюда',
                                  related_name='recipes',
                                  through='MealTypeRecipe',
                                  )
    people = models.IntegerField(verbose_name='Количество порций', default=1)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name

    def get_total_weight_per_person(self):
        return sum([ingredient_item.quantity
             for ingredient_item in self.recipe_ingredients.all()]) / self.people

    def get_total_calories(self):
        return sum([ingredient_item.quantity * (ingredient_item.ingredient.energy / 100)
                    for ingredient_item in self.recipe_ingredients.all()])

    def get_total_calories_per_100(self):
        return self.get_total_calories() / sum([ingredient_item.quantity
                                                for ingredient_item in self.recipe_ingredients.all()])

    def get_total_calories_per_person(self):
        return int(self.get_total_calories() / self.people)


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
    quantity = models.IntegerField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'

    def __str__(self):
        return f'{self.ingredient} - {self.quantity}'


class MealTypeRecipe(models.Model):
    meal_type = models.ForeignKey(MealType,
                                  on_delete=models.PROTECT,
                                  verbose_name='Тип блюда',
                                  related_name='meal_type_recipes',
                                  )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.PROTECT,
                               verbose_name='Рецепт',
                               related_name='meal_type_recipes',
                               )

    class Meta:
        verbose_name = 'тип блюда'
        verbose_name_plural = 'Рецепты по типам блюд'

    def __str__(self):
        return f'{self.meal_type} - {self.recipe}'


class MenuTypeRecipe(models.Model):
    menu_type = models.ForeignKey(MenuType,
                                  on_delete=models.PROTECT,
                                  verbose_name='Тип меню',
                                  related_name='menu_type_recipes',
                                  )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.PROTECT,
                               verbose_name='Рецепт',
                               related_name='menu_type_recipes',
                               )

    class Meta:
        verbose_name = 'тип меню'
        verbose_name_plural = 'Рецепты по типам меню'

    def __str__(self):
        return f'{self.menu_type} - {self.recipe}'


class Subscription(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('waiting_for_payment', 'Ожидает оплаты'),
        ('paid', 'Оплачено'),
        ('canceled', 'Отменено'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь',
                             related_name='subscriptions',
                             )
    menu_type = models.ForeignKey(MenuType,
                                  on_delete=models.PROTECT,
                                  verbose_name='Тип меню',
                                  related_name='subscriptions',
                                  )
    people_quantity = models.IntegerField(verbose_name='Количество персон')
    meal_type = models.ManyToManyField(MealType,
                                       verbose_name='Тип блюда',
                                       related_name='subscriptions',
                                       through='SubscriptionMealType',
                                       )
    allergies = models.ManyToManyField(Allergy,
                                     verbose_name='Аллергия',
                                     related_name='subscriptions',
                                     through='SubscriptionAllergy',
                                     )
    total_price = models.DecimalField(max_digits=8,
                                      decimal_places=2,
                                      verbose_name='Стоимость, руб.',
                                      )
    payment_status = models.CharField(max_length=20,
                                      verbose_name='Статус оплаты',
                                      choices=PAYMENT_STATUS_CHOICES,
                                      default='waiting_for_payment',
                                      )
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user}: {self.start_date} - {self.end_date}'

    def get_recipes(self):
        return self.menu_type.recipes.all()


class SubscriptionMealType(models.Model):
    subscription = models.ForeignKey(Subscription,
                                     on_delete=models.PROTECT,
                                     verbose_name='Подписка',
                                     related_name='subscription_meal_types',
                                     )
    meal_type = models.ForeignKey(MealType,
                                  on_delete=models.PROTECT,
                                  verbose_name='Тип блюда',
                                  related_name='subscription_meal_types',
                                  )

    class Meta:
        verbose_name = 'Тип блюда подписки'
        verbose_name_plural = 'Типы блюд подписки'

    def __str__(self):
        return f'{self.subscription} - {self.meal_type}'


class SubscriptionAllergy(models.Model):
    subscription = models.ForeignKey(Subscription,
                                     on_delete=models.PROTECT,
                                     verbose_name='Подписка',
                                     related_name='subscription_allergies',
                                     )
    allergy = models.ForeignKey(Allergy,
                                on_delete=models.PROTECT,
                                verbose_name='Аллергия',
                                related_name='subscription_allergies',
                                )

    class Meta:
        verbose_name = 'Аллергия в подписке'
        verbose_name_plural = 'Аллергии в подписке'

    def __str__(self):
        return f'{self.subscription} - {self.allergy}'


class UserRecipe(models.Model):
    REACTION_CHOICES = (
        ('like', 'Нравится'),
        ('dislike', 'Не нравится'),
        ('neutral', 'Нейтрально'),
    )
    date = models.DateField(verbose_name='Дата')
    subscription = models.ForeignKey(Subscription,
                                        on_delete=models.PROTECT,
                                        verbose_name='Подписка',
                                        related_name='user_recipes',
                                        )
    meal_type = models.ForeignKey(MealType,
                                  on_delete=models.PROTECT,
                                  verbose_name='Тип блюда',
                                  related_name='user_recipes',
                                  )
    multiplier = models.IntegerField(verbose_name='Множитель', default=1)
    attempt = models.IntegerField(verbose_name='Попытка', default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT,
                             verbose_name='Пользователь',
                             related_name='user_recipes',
                             )
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.PROTECT,
                               verbose_name='Рецепт',
                               related_name='user_recipes',
                               )
    reaction = models.CharField(max_length=7, verbose_name='Реакция', choices=REACTION_CHOICES, default='neutral')
    is_valid = models.BooleanField(verbose_name='Действует', default=True)

    class Meta:
        verbose_name = 'Рецепт пользователя'
        verbose_name_plural = 'Рецепты пользователей по дням'

    def __str__(self):
        return f'{self.user} - {self.recipe}'

    def get_total_people(self):
        return self.recipe.people * self.multiplier

    def get_total_ingredients(self):
        total_ingredients = []
        for ingredient in self.recipe.recipe_ingredients.all():
            total_ingredients.append({
                'ingredient': ingredient.ingredient,
                'quantity': ingredient.quantity * self.multiplier,
            })
        return total_ingredients
