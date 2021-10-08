import os

from django.core.management import BaseCommand
from django.template import Template, Context
import pathlib


class Command(BaseCommand):
    help = 'Rebuild indexes'

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.data = {}
        self.context = None

    def add_arguments(self, parser):
        parser.add_argument('model', type=str)
        parser.add_argument('fields', type=str)

    def write_data(self, file_name_read, file_name_write):
        with open(f'{pathlib.Path(__file__).parent.resolve()}/{file_name_read}', 'r') as f:
            template = Template(f.read())
            data = template.render(self.context)
            with open(f'api/{self.data["model_name_plural_lower"]}/{file_name_write}', 'w') as file:
                file.write(data)

    def handle(self, *args, **options):
        self.data["model_name"] = options['model'].capitalize()
        self.data["model_name_lower"] = self.data["model_name"].lower()
        self.data["fields"] = ''
        for field in options['fields'].split(','):
            self.data["fields"] += f'\'{field}\','

        self.data["returned_fields"] = self.data["fields"] + '\'id\','
        self.data["model_plural_name"] = f'{self.data["model_name"]}s'
        self.data["model_name_plural_lower"] = self.data["model_plural_name"].lower()
        model_directory = f'api/{self.data["model_name_plural_lower"]}'
        self.data["fields_for_model"] = ''

        for field in options['fields'].split(','):
            self.data["fields_for_model"] += '\t' + field + ' = models' + '\n'

        self.context = Context(self.data)

        if not os.path.isdir('api/' + self.data["model_name_plural_lower"]):
            os.makedirs('api/' + self.data["model_name_plural_lower"])

        self.write_data('default_serializer.txt', 'serializers.py')
        self.stdout.write(self.style.SUCCESS('Serializer was successfully created'))
        self.write_data('default_model.txt', 'models.py')
        self.stdout.write(self.style.SUCCESS('Model was successfully created'))
        self.write_data('default_view.txt', 'views.py')
        self.stdout.write(self.style.SUCCESS('View was successfully created'))
        self.write_data('default_urls.txt', 'urls.py')
        self.stdout.write(self.style.SUCCESS('Urls was successfully created'))
        open(model_directory + '/helper.py', 'a').close()
        self.stdout.write(self.style.SUCCESS('Helper was successfully created'))
        open(model_directory + '/tests.py', 'a').close()
        self.stdout.write(self.style.SUCCESS('tests was successfully created'))
        open(model_directory + '/__init__.py', 'a').close()
