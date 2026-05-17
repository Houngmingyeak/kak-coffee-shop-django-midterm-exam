from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Coffee
from .forms import CoffeeForm


class CoffeeModelTest(TestCase):
    def setUp(self):
        self.coffee = Coffee.objects.create(
            name='Espresso',
            category='espresso',
            description='Strong and bold',
            price=Decimal('3.50'),
            is_available=True,
        )

    def test_coffee_str(self):
        self.assertEqual(str(self.coffee), 'Espresso ($3.50)')

    def test_coffee_fields(self):
        self.assertEqual(self.coffee.name, 'Espresso')
        self.assertEqual(self.coffee.category, 'espresso')
        self.assertEqual(self.coffee.price, Decimal('3.50'))
        self.assertTrue(self.coffee.is_available)

    def test_default_availability(self):
        coffee = Coffee.objects.create(name='Test', price=Decimal('2.00'))
        self.assertTrue(coffee.is_available)


class CoffeeFormTest(TestCase):
    def test_valid_form(self):
        data = {
            'name': 'Latte',
            'category': 'latte',
            'description': 'Creamy and smooth',
            'price': '4.50',
            'is_available': True,
        }
        form = CoffeeForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_price(self):
        data = {
            'name': 'Bad Coffee',
            'category': 'other',
            'price': '-1.00',
            'is_available': True,
        }
        form = CoffeeForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_missing_name(self):
        data = {'price': '3.00', 'is_available': True}
        form = CoffeeForm(data=data)
        self.assertFalse(form.is_valid())


class CoffeeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.coffee = Coffee.objects.create(
            name='Cappuccino',
            category='cappuccino',
            price=Decimal('4.00'),
            is_available=True,
        )

    def test_coffee_list_view(self):
        response = self.client.get(reverse('coffee_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cappuccino')

    def test_add_coffee_get(self):
        response = self.client.get(reverse('add_coffee'))
        self.assertEqual(response.status_code, 200)

    def test_add_coffee_post(self):
        data = {
            'name': 'Cold Brew',
            'category': 'cold_brew',
            'description': 'Smooth and refreshing',
            'price': '5.00',
            'is_available': True,
        }
        response = self.client.post(reverse('add_coffee'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Coffee.objects.filter(name='Cold Brew').exists())

    def test_update_coffee(self):
        data = {
            'name': 'Cappuccino Deluxe',
            'category': 'cappuccino',
            'description': 'Updated',
            'price': '4.50',
            'is_available': True,
        }
        response = self.client.post(
            reverse('update_coffee', kwargs={'pk': self.coffee.pk}), data
        )
        self.assertEqual(response.status_code, 302)
        self.coffee.refresh_from_db()
        self.assertEqual(self.coffee.name, 'Cappuccino Deluxe')

    def test_delete_coffee(self):
        response = self.client.post(
            reverse('delete_coffee', kwargs={'pk': self.coffee.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Coffee.objects.filter(pk=self.coffee.pk).exists())

    def test_search_filter(self):
        response = self.client.get(reverse('coffee_list'), {'q': 'Cappuccino'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cappuccino')
