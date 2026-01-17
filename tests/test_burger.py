import pytest
from unittest.mock import Mock
from test_data.burger_data import move_ingredient_params


class TestBurger:
    """Тесты для класса Burger"""

    def test_init_creates_burger_without_bun(self, burger):
        """Инициализация создает бургер с bun=None"""
        assert burger.bun is None

    def test_init_creates_burger_without_ingredients(self, burger):
        """Инициализация создает бургер с пустым списком ингредиентов"""
        assert burger.ingredients == []

    def test_set_buns_correctly(self, burger, mock_bun):
        """Установка булочки сохраняет объект"""
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient_to_list(self, burger, parametrized_ingredient):
        """Ингредиент добавляется в список бургера"""
        burger.add_ingredient(parametrized_ingredient)
        assert burger.ingredients == [parametrized_ingredient]

    def test_remove_ingredient_by_valid_index_removes_item(self, burger, parametrized_ingredient):
        """Удаление по индексу удаляет конкретный ингредиент из списка"""
        burger.add_ingredient(parametrized_ingredient)
        burger.remove_ingredient(0)
        assert burger.ingredients == []

    @pytest.mark.parametrize("index,new_index", move_ingredient_params)
    def test_move_ingredient_changes_position(self, burger, three_different_ingredients, index, new_index):
        """Ингредиент перемещается с index на new_index"""
        burger.ingredients = list(three_different_ingredients)
        ingredient_to_move = burger.ingredients[index]
        burger.move_ingredient(index, new_index)
        assert burger.ingredients[new_index] == ingredient_to_move

    def test_get_price_without_bun_raises_error(self, burger, parametrized_ingredient):
        """Цена без булочки вызывает ошибку"""
        burger.add_ingredient(parametrized_ingredient)
        with pytest.raises(AttributeError):
            burger.get_price()

    def test_get_price_calculates_correctly(self, burger, mock_bun, parametrized_ingredient):
        """Цена = булочка * 2 + ингредиенты"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(parametrized_ingredient)
        expected = mock_bun.get_price() * 2 + parametrized_ingredient.get_price()
        assert burger.get_price() == expected

    def test_get_receipt_without_ingredients(self, burger, mock_bun):
        """Чек без ингредиентов: 2 булочки + цена"""
        burger.set_buns(mock_bun)
        receipt = burger.get_receipt()
        bun_name = mock_bun.get_name()
        assert f'(==== {bun_name} ====' in receipt
        assert receipt.count(f'(==== {bun_name} ====)') == 2
        assert "Price:" in receipt

    def test_get_receipt_with_ingredients(self, burger, mock_bun, parametrized_ingredient):
        """Чек с ингредиентами: булочки + ингредиент + цена"""
        burger.set_buns(mock_bun)
        burger.add_ingredient(parametrized_ingredient)
        burger.get_price = Mock(return_value=350.0)
        receipt = burger.get_receipt()
        expected_receipt = (
            f"(==== {mock_bun.get_name()} ====)\n"
            f"= {parametrized_ingredient.get_type().lower()} {parametrized_ingredient.get_name()} =\n"
            f"(==== {mock_bun.get_name()} ====)\n\n"
            "Price: 350.0"
        )
        assert receipt == expected_receipt
