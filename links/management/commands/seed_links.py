"""
Seed the Links table with Linktree / Link-in-Bio entries.

Usage:
    python manage.py seed_links
    python manage.py seed_links --clear   # wipe existing rows first
"""

from django.core.management.base import BaseCommand
from links.models import Link

SEED_DATA = [
    {
        "sortorder": 10,
        "label": "rps.org/hellenvanMeene",
        "url": "https://rps.org/hellenvanMeene",
        "description": (
            "RPS Awards Talks — Hellen van Meene with Martin Barnes. "
            "Wednesday, 6 July 2022, 1800–1900 (BST) | 1900–2000 (CET) | 1300–1400 (EST)"
        ),
    },
    {
        "sortorder": 20,
        "label": '"Quickenings" exhibition at James Freeman Gallery, London',
        "url": "https://www.jamesfreemangallery.com/exhibitions/quickenings/",
        "description": (
            "Quickenings, an online exhibition exploring themes of Nature, transformation, "
            "and the anticipation of change through the work of four contemporary artists: "
            "Andy Harper, Charles Freger, Hellen van Meene, and Richard Stone."
        ),
    },
    {
        "sortorder": 30,
        "label": "yanceyrichardson.viewingrooms.com",
        "url": (
            "https://yanceyrichardson.viewingrooms.com/viewing-room/"
            "6-reverberation-sharon-core-jitka-hanzlova-ori-gersht-and-hellen/"
        ),
        "description": "Yancey Richardson's Reverberation Exhibition on viewingrooms.com",
    },
    {
        "sortorder": 40,
        "label": "www.welikeart.nl/product/hellen-van-meene-3",
        "url": "https://www.welikeart.nl/product/hellen-van-meene-3/",
        "description": (
            "Koop #0474, limited edition (2020) bij We Like Art! "
            "Gespreid betalen met de KunstKoop mogelijk."
        ),
    },
    {
        "sortorder": 50,
        "label": "hellenvanmeene.com/shop",
        "url": "http://hellenvanmeene.com/shop",
        "description": "Buy her Limited Edition of #0474 in edition of 25!",
    },
    {
        "sortorder": 60,
        "label": "hellenvanmeene.com",
        "url": "http://hellenvanmeene.com/",
        "description": "",
    },
    {
        "sortorder": 70,
        "label": "www.galeriefontana.com",
        "url": "https://www.galeriefontana.com/",
        "description": "Galerie Fontana, Amsterdam, Netherlands",
    },
    {
        "sortorder": 80,
        "label": "www.jamesfreemangallery.com",
        "url": "https://www.jamesfreemangallery.com/",
        "description": "James Freeman Gallery, London, UK",
    },
    {
        "sortorder": 90,
        "label": "www.gallerykoyanagi.com",
        "url": "http://www.gallerykoyanagi.com/",
        "description": "Gallery Koyanagi, Tokyo, Japan",
    },
    {
        "sortorder": 100,
        "label": "www.yanceyrichardson.com",
        "url": "http://www.yanceyrichardson.com/",
        "description": "Yancey Richardson Gallery, New York, NY, USA",
    },
]


class Command(BaseCommand):
    help = "Seed the Links table with Linktree / Link-in-Bio entries."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing links before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted, _ = Link.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted} existing link(s)."))

        created_count = 0
        updated_count = 0

        for entry in SEED_DATA:
            obj, created = Link.objects.update_or_create(
                url=entry["url"],
                defaults={
                    "label": entry["label"],
                    "description": entry["description"],
                    "sortorder": entry["sortorder"],
                    "do_not_show": False,
                },
            )
            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Done — {created_count} created, {updated_count} updated."
            )
        )
