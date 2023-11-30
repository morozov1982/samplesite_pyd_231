import os
import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from bboard.models import Rubric, Bb


JSON_PATH = os.path.join('bboard', 'fixtures')


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name), mode='r', encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        rubrics = load_from_json('rubrics.json')
        bbs = load_from_json('bbs.json')

        # Bb.objects.all().delete()
        # Rubric.objects.all().delete()
        # User.objects.all().delete()

        for rubric in rubrics:
            _rubric = rubric.get('fields')
            _rubric['id'] = rubric.get('pk')
            new_rubric = Rubric(**_rubric)
            new_rubric.save()

        for bb in bbs:
            _bb = bb.get('fields')
            rubric_id = _bb.get('rubric')
            _bb['rubric'] = Rubric.objects.get(id=rubric_id)
            new_bb = Bb(**_bb)
            new_bb.save()

        User.objects.create_superuser('admin', 'admin@bboard.local', '123')
