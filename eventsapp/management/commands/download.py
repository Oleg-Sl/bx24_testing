import pprint
from django.core.management.base import BaseCommand
from django.utils import timezone

from bitrix24 import tokens, requests

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        files_objects = {
                "441": {
                    "ATTACHMENT_ID": "441",
                    "NAME": "example.jpeg",
                    "SIZE": "6333",
                    "FILE_ID": "3119",
                    "DOWNLOAD_URL": "/bitrix/tools/disk/uf.php?attachedId=441&auth%5Baplogin%5D=9&auth%5Bap%5D=vhduvllk2mxru5lx&action=download&ncc=1",
                    "VIEW_URL": "/bitrix/tools/disk/uf.php?attachedId=441&auth%5Baplogin%5D=9&auth%5Bap%5D=vhduvllk2mxru5lx&action=show&ncc=1"
                },
                "443": {
                    "ATTACHMENT_ID": "443",
                    "NAME": "example.png",
                    "SIZE": "34983",
                    "FILE_ID": "3121",
                    "DOWNLOAD_URL": "/bitrix/tools/disk/uf.php?attachedId=443&auth%5Baplogin%5D=9&auth%5Bap%5D=vhduvllk2mxru5lx&action=download&ncc=1",
                    "VIEW_URL": "/bitrix/tools/disk/uf.php?attachedId=443&auth%5Baplogin%5D=9&auth%5Bap%5D=vhduvllk2mxru5lx&action=show&ncc=1"
                }
            }

        bx24 = requests.Bitrix24()

        for _, f_data in files_objects.items():
            f_path = bx24.download_file(f_data.get("DOWNLOAD_URL"))
