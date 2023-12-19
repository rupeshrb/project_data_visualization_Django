import json
from django.core.management.base import BaseCommand
from main.models import InternData

class Command(BaseCommand):
    help = 'Load data from JSON file into InternData model'

    def handle(self, *args, **options):
        json_file_path = 'P:\\Internship Assignment\\Assingment on data Visualization\\jsondata.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Clear existing data (optional)
            InternData.objects.all().delete()

            # Bulk insert new data
            objects_to_create = []

            for item in data:
                # Convert 'end_year' and 'start_year' to string and strip leading/trailing spaces
                item['end_year'] = str(item['end_year']).strip() if item['end_year'] is not None else None
                item['start_year'] = str(item['start_year']).strip() if item['start_year'] is not None else None

                # Handle 'intensity', 'likelihood', and 'relevance' fields
                try:
                    item['intensity'] = int(item['intensity'])
                except (ValueError, TypeError):
                    item['intensity'] = None

                try:
                    item['likelihood'] = int(item['likelihood'])
                except (ValueError, TypeError):
                    item['likelihood'] = None

                try:
                    item['relevance'] = int(item['relevance'])
                except (ValueError, TypeError):
                    item['relevance'] = None

                objects_to_create.append(InternData(**item))

            InternData.objects.bulk_create(objects_to_create)

            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
