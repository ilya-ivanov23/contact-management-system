from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.core.cache import cache
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Contact, ContactStatusChoices
from .utils import get_weather_for_city

class ContactModelTest(TestCase):
    def setUp(self):
        self.status = ContactStatusChoices.objects.create(name='New')
        self.contact = Contact.objects.create(
            first_name='Jan',
            last_name='Kowalski',
            phone_number='+48123456789',
            email='jan.kowalski@example.com',
            city='Warsaw',
            status=self.status
        )

    def test_contact_creation(self):
        self.assertEqual(self.contact.first_name, 'Jan')
        self.assertEqual(str(self.contact), 'Jan Kowalski')
        self.assertEqual(str(self.status), 'New')


class ContactAPITest(APITestCase):
    def setUp(self):
        self.status = ContactStatusChoices.objects.create(name='In Progress')
        self.contact = Contact.objects.create(
            first_name='Anna',
            last_name='Nowak',
            phone_number='+48987654321',
            email='anna.nowak@example.com',
            city='Krakow',
            status=self.status
        )

    def test_get_contacts_api(self):
        response = self.client.get('/api/contacts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'Anna')

    def test_create_contact_api(self):
        data = {
            'first_name': 'Piotr',
            'last_name': 'Zieliński',
            'phone_number': '+48555666777',
            'email': 'piotr.zielinski@example.com',
            'city': 'Gdańsk',
            'status': self.status.id
        }
        response = self.client.post('/api/contacts/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contact.objects.count(), 2)


class WeatherUtilityTest(TestCase):
    def setUp(self):
        cache.clear()

    @patch('requests.get')
    def test_get_weather_for_city_success(self, mock_get):
        mock_nominatim = MagicMock()
        mock_nominatim.status_code = 200
        mock_nominatim.json.return_value = [{'lat': '52.22977', 'lon': '21.01178'}]

        mock_weather = MagicMock()
        mock_weather.status_code = 200
        mock_weather.json.return_value = {
            'current': {
                'temperature_2m': 20.5,
                'relative_humidity_2m': 60,
                'wind_speed_10m': 15.0
            }
        }

        mock_get.side_effect = [mock_nominatim, mock_weather]

        weather_data = get_weather_for_city('Warsaw')
        self.assertIsNotNone(weather_data)
        self.assertEqual(weather_data['temperature'], 20.5)
        self.assertEqual(weather_data['humidity'], 60)
        self.assertEqual(weather_data['windspeed'], 15.0)

    def test_get_weather_empty_city(self):
        self.assertIsNone(get_weather_for_city(''))
