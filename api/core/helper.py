import json
import math
import urllib.parse

import pendulum
import requests
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.utils.translation import gettext as _


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_time_zone(request):
    ip = '104.236.53.155'
    geo_information = GeoIP2()
    info = geo_information.city(ip)
    time_zone = info['time_zone']
    return time_zone


def tz_diff(home, away):
    dt_home = pendulum.datetime(2020, 1, 1, tz=home)
    dt_client = pendulum.datetime(2020, 1, 1, tz=away)
    diff = dt_home.diff(dt_client).in_hours()

    if abs(diff) > 12.0:
        if diff < 0.0:
            diff += 24.0
        else:
            diff -= 24.0

    return diff


def get_model_fields(model):
    fields = [f.name for f in model._meta.get_fields()]  # noqa
    model_fields = tuple()
    for field in fields:
        model_fields += (field, _(field))
    return model_fields


def get_date_by_age(age):
    current_year = pendulum.now().format('Y')  # noqa
    current_month = pendulum.now().format('M')  # noqa
    current_day = pendulum.now().format('D')  # noqa
    year_by_age = int(current_year) - int(age)
    date = pendulum.date(year=year_by_age, month=int(current_month), day=int(current_day))
    return date


def get_age_by_date(date):
    current_year = pendulum.now().format('Y')  # noqa
    year = pendulum.from_format(date, 'YYYY-MM-DD').format('Y')  # noqa
    age_by_year = int(current_year) - int(year)
    return age_by_year


def get_date_for_range(date):
    if date[0] < date[1]:
        date_to_swap = get_date_by_age(date[1])
        date[1] = get_date_by_age(date[0])
        date[0] = date_to_swap
    else:
        date[0] = get_date_by_age(date[0])
        date[1] = get_date_by_age(date[1])
    return date


def get_filters_by_conditions(contact_group):
    set_filter = {}
    for value in contact_group.custom_query:
        column = json.loads(value).get('column')
        if json.loads(value).get('condition') == 'e':
            condition = column
        else:
            condition = column + '__' + json.loads(value).get('condition')
        value = json.loads(value).get('value')
        set_filter.update({condition: value})

    return set_filter


def get_sms_count(contact_groups, queryset):
    sms_count = 0

    for contact_group in contact_groups.all():
        if contact_group.use_query:
            filters = get_filters_by_conditions(contact_group)
            sms_count = len(queryset.filter(**filters).values_list('id', flat=True))
        else:
            sms_count = len(contact_group.contacts.all().values_list('id', flat=True))

    return sms_count


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def get_sms_count_and_phone_numbers(message, values, variables):
    number_of_characters_per_message = settings.NUMBER_OF_CHARACTERS
    sms_count = 0
    phone_numbers = 0
    used_phone_numbers = []
    for information_about_client in values:
        message_to_send = message
        for variable in variables:
            variable_to_remove = variable.replace('{{', '').replace('}}', '')
            if '{{age}}' in message_to_send and information_about_client['birth_date']:
                age = get_age_by_date(str(information_about_client['birth_date']))
                message_to_send = message_to_send.replace('{{age}}', str(age))
            elif '{{age}}' in message_to_send:
                message_to_send = message_to_send.replace('{{age}}', '')
            if variable in message_to_send and information_about_client[variable_to_remove]:
                message_to_send = message_to_send.replace(variable, str(information_about_client[variable_to_remove]))
            elif variable in message_to_send:
                message_to_send = message_to_send.replace(variable, '')
        message_to_send = urllib.parse.quote(message_to_send)
        if information_about_client['phone_number'] not in used_phone_numbers:
            used_phone_numbers.append(information_about_client['phone_number'])
            sms_count += int(round_up(len(message_to_send) / number_of_characters_per_message))
            phone_numbers += 1
    return phone_numbers, sms_count


def send_sms_to_all(message, values, setting):
    number_of_characters_per_message = settings.NUMBER_OF_CHARACTERS
    sms_count = 0
    phone_numbers = 0
    used_phone_numbers = []
    for information_about_client in values:
        # message_to_send = prepare_message(message, information_about_client)
        message_to_send = urllib.parse.quote(message_to_send)
        if information_about_client['phone_number'] not in used_phone_numbers:
            used_phone_numbers.append(information_about_client['phone_number'])
            sms_count += int(round_up(len(message_to_send) / number_of_characters_per_message))
            phone_numbers += 1
            params = {
                'username': setting.username,
                'password': setting.password,
                'from': 'oklyx',
                'to': information_about_client['phone_number'],
                'text': message_to_send
            }
            url = 'https://193.16.111.11/sms.asp?'
            for value, label in params.items():
                url += '&%s=%s' % (value, label)
            requests.get(url, verify=False)  # noqa

    return phone_numbers, sms_count


def file_name(self, filename):
    return '/'.join(['file', filename])


def image_name(self, filename):
    return '/'.join(['images', filename])
