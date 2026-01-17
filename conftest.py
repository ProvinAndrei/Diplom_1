import pytest
from unittest.mock import Mock
from praktikum.bun import Bun
from praktikum.burger import Burger
from praktikum.ingredient import Ingredient
from test_data.burger_data import buns_data, ingredients_data

@pytest.fixture
def burger():
    """Фикстура для создания бургера"""
    return Burger()

@pytest.fixture
def mock_bun():
    """Мок булочки с методами get_name и get_price"""
    bun_mock = Mock(spec=Bun)
    bun_mock.get_name.return_value = "test bun"
    bun_mock.get_price.return_value = 100.0
    return bun_mock

@pytest.fixture(params=buns_data)
def parametrized_bun(request):
    """Параметризованная булочка из test_data"""
    name, price = request.param
    return Bun(name, price)

@pytest.fixture(params=ingredients_data)
def parametrized_ingredient(request):
    """Параметризованный ингредиент из test_data"""
    type_, name, price = request.param
    return Ingredient(type_, name, price)

@pytest.fixture
def three_different_ingredients():
    """Три разных ингредиента из burger_data"""
    return [Ingredient(*data) for data in ingredients_data[:3]]
