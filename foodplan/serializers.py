from rest_framework.serializers import ModelSerializer, CharField, IntegerField, FloatField, SerializerMethodField

from .models import UserRecipe, Recipe, Subscription, SubscriptionMealType, Allergy, MenuType, MealType, Ingredient, \
    Unit


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class IngredientSerializer(ModelSerializer):
    unit_name = CharField(source='unit.name', read_only=True)

    class Meta:
        model = Ingredient
        fields = '__all__'


class AllergySerializer(ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'


class MealTypeSerializer(ModelSerializer):
    class Meta:
        model = MealType
        fields = '__all__'



class MenuTypeSerializer(ModelSerializer):
    class Meta:
        model = MenuType
        fields = '__all__'


class SubscriptionSerializer(ModelSerializer):
    allergies = AllergySerializer(many=True, read_only=True, allow_empty=True)
    meal_type = MealTypeSerializer(many=True, read_only=True, allow_empty=False)
    menu_type = MenuTypeSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = '__all__'


class RecipeSerializer(ModelSerializer):
    total_calories_per_person = IntegerField(source='get_total_calories_per_person', read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class UserRecipeSerializer(ModelSerializer):
    subscription = SubscriptionSerializer(read_only=True)
    recipe = RecipeSerializer(read_only=True)
    meal_type = MealTypeSerializer(read_only=True)
    user_pk = IntegerField(source='user.pk', read_only=True)
    total_ingredients = SerializerMethodField()
    total_people = IntegerField(source='get_total_people', read_only=True)

    class Meta:
        model = UserRecipe
        fields = [
            'id',
            'user_pk',
            'subscription',
            'recipe',
            'meal_type',
            'date',
            'is_valid',
            'reaction',
            'total_ingredients',
            'total_people',
        ]

    def get_total_ingredients(self, obj):
        ingredients_serializer = IngredientSerializer(
            instance=[item['ingredient'] for item in obj.get_total_ingredients()],
            many=True
        )
        total_ingredients = ingredients_serializer.data

        # Добавляем количества
        for item, ingredient in zip(obj.get_total_ingredients(), total_ingredients):
            ingredient['quantity'] = item['quantity']

        return total_ingredients

