import csv
import io
from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework import viewsets
from .models import Contact, ContactStatusChoices
from .serializers import ContactSerializer
from .utils import get_weather_for_city

# --- REST API Views ---

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

# --- Web UI Views ---

def contact_list(request):
    sort_by = request.GET.get('sort', 'last_name')
    
    # Simple validation to prevent invalid sort parameters
    if sort_by not in ['last_name', '-created_at']:
        sort_by = 'last_name'

    contacts = Contact.objects.all().select_related('status').order_by(sort_by)

    # Attach weather data to each contact
    for contact in contacts:
        weather_data = get_weather_for_city(contact.city)
        contact.weather = weather_data

    context = {
        'contacts': contacts,
        'current_sort': sort_by
    }
    return render(request, 'contacts/contact_list.html', context)

def import_csv(request):
    if request.method == 'POST':
        if 'csv_file' not in request.FILES:
            messages.error(request, 'No file was uploaded.')
            return redirect('contact_list')

        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'This is not a CSV file.')
            return redirect('contact_list')

        try:
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            # Skip the header row
            reader = csv.DictReader(io_string)

            imported_count = 0
            for row in reader:
                # We expect columns: first_name, last_name, phone_number, email, city, status
                # Here we assume the status column matches the string name of a ContactStatusChoices
                status_name = row.get('status', 'New')
                status_obj, _ = ContactStatusChoices.objects.get_or_create(name=status_name)

                email = row.get('email')
                phone_number = row.get('phone_number')

                # Update or create the contact using email and phone number as primary unique identifiers
                # Assuming email is unique as per model definition
                if email and phone_number:
                    Contact.objects.update_or_create(
                        email=email,
                        defaults={
                            'first_name': row.get('first_name', ''),
                            'last_name': row.get('last_name', ''),
                            'phone_number': phone_number,
                            'city': row.get('city', ''),
                            'status': status_obj
                        }
                    )
                    imported_count += 1
            
            messages.success(request, f'Successfully imported {imported_count} contacts.')

        except Exception as e:
            messages.error(request, f'Error parsing CSV file: {str(e)}')

    return redirect('contact_list')
