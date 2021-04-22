from django.core.management.base import BaseCommand, CommandError
from main import models
from django.conf import settings
import os, datetime
from tqdm import tqdm

DIR = os.path.join(settings.MEDIA_ROOT, "secure/documents")

class Command(BaseCommand):
    help = 'Checks all documents in media/secure/documents folder for existing in DB'

    def add_arguments(self, parser):
        parser.add_argument('-days', type=int, default=7)

    def handle(self, *args, **options):
        print("Checking all files...")
        all_files = os.listdir(DIR)

        now = datetime.datetime.now()
        days = options['days']
        ago = now-datetime.timedelta(days=days)
        print(f"Finded total {len(all_files)} files, searching for new (days before:{days})...")

        target_files = []
        for file in all_files:
            path = os.path.join(DIR, file)
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path))
            if mtime > ago:
                target_files.append(path)
        
        print(f"Finded {len(target_files)} newly modified files, checking them in DB")
        R = input("Press Y and enter if you confirm adding to DB ->")
        if not R.lower() == "y":
            raise RuntimeError("Not confirmed")

        non_ex = 0
        for file in tqdm(target_files, unit="file"):
            relp = os.path.relpath(file, settings.MEDIA_ROOT)
            # print(relp)
            try:
                doc = models.Document.objects.get(file=relp.replace('\\', '/'))
            except models.Document.DoesNotExist:
                exists = False
                non_ex += 1
            else:
                exists = True
            # print(exists)
            if not exists:
                models.Document.objects.create(file=relp, approved=None)
            #     break
                # print('-- Finded ')
        print("Total non exists:", non_ex)
