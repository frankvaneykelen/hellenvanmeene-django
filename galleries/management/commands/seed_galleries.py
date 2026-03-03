"""
Seed the Galleries table with the four galleries that represent Hellen van Meene.

Usage:
    python manage.py seed_galleries
    python manage.py seed_galleries --clear   # wipe existing rows first
"""

from django.core.management.base import BaseCommand

from core.models import Country, Place
from galleries.models import Gallery

SEED_DATA = [
    {
        "slug": "galerie-fontana",
        "name": "Galerie Fontana",
        "city": "Amsterdam",
        "country": "Netherlands",
        "description": (
            "Galerie Fontana, founded in 2011 and based in a former chocolate factory "
            "in Amsterdam, showcases contemporary art with a focus on humanity, "
            "vulnerability, and mortality. The gallery represents both emerging and "
            "established artists, participating in international art fairs and exhibitions.\n\n"
            "Fontana aims to connect people through art, emphasizing strong personal "
            "connections with both the artwork and the artists."
        ),
        "website": "https://www.galeriefontana.com/",
        "phone": "+31 20 22 3 88 33",
        "phone2": "+31 6 21 57 80 45",
        "image_link": "/cloud/website-images/galerie-fontana.jpg",
        "image_alt": "Galerie Fontana",
        "sortorder": 10,
    },
    {
        "slug": "james-freeman-gallery",
        "name": "James Freeman Gallery",
        "city": "London",
        "country": "United Kingdom",
        "description": (
            "James Freeman Gallery is a contemporary art dealer based in Islington, "
            "London, UK.\n\n"
            "Established in 2003, the gallery explores contemporary approaches to "
            "classicism, presenting artists who combine current tendencies with "
            "art-historical references and research. In particular, the gallery aims "
            "to present artists who do this in a way that is both aesthetically "
            "powerful & technically accomplished.\n\n"
            "The gallery programme presents a mixture of solo exhibitions and curated "
            "group shows that explore this historical focus. As well as exhibiting "
            "established artists, they often work with younger artists to give them "
            "an early platform to present and develop their practice.\n\n"
            "Over the years the gallery has exhibited at a global level, including "
            "fairs and gallery collaborations in the USA, Europe and Asia."
        ),
        "website": "https://www.jamesfreemangallery.com/",
        "phone": "+44 20 7226 3300",
        "phone2": "",
        "image_link": "/cloud/website-images/james-freeman-gallery.jpg",
        "image_alt": "Hellen van Meene standing in front of James Freeman Gallery",
        "sortorder": 20,
    },
    {
        "slug": "gallery-koyanagi",
        "name": "Gallery Koyanagi",
        "city": "Tokyo",
        "country": "Japan",
        "description": (
            "Founded in Ginza, Tokyo in 1995. "
            "Gallery artists include Hiroshi Sugimoto, Marlene Dumas, Sophie Calle, "
            "Olafur Eliasson, Christian Marclay, Thomas Ruff, Hellen van Meene, "
            "Rei Naito, Noguchi Rika, Yoshihiro Suda and Tabaimo.\n\n"
            "Exhibitor at Art Basel since 2000."
        ),
        "website": "http://www.gallerykoyanagi.com/",
        "phone": "+81 3 35611896",
        "phone2": "",
        "image_link": "/cloud/website-images/koyanagi-hvm_insta_01_m.jpg",
        "image_alt": "Gallery Koyanagi (installation view of a Hellen van Meene exhibition)",
        "sortorder": 30,
    },
    {
        "slug": "yancey-richardson-gallery",
        "name": "Yancey Richardson Gallery",
        "city": "New York",
        "country": "United States",
        "description": (
            "Founded in 1995, the Yancey Richardson Gallery is one of the preeminent "
            "dealers of fine art photography in the US. Yancey Richardson brings over "
            "30 years of experience to the gallery's exhibition program, and is a member "
            "of the Art Dealers Association of America (ADAA). The gallery is located "
            "in the heart of New York's Chelsea art district.\n\n"
            "The gallery's program includes critically recognized, emerging photographers "
            "such as Bryan Graf, Zanele Muholi and Victoria Sambunaris, as well as "
            "established mid-career artists such as Sharon Core, Mitch Epstein, "
            "Laura Letinsky, Andrew Moore, Sebastiao Salgado and Hellen van Meene. "
            "Additionally, the gallery regularly exhibits the work of established "
            "masters, including August Sander, Ed Ruscha, William Eggleston, and "
            "Robert Mapplethorpe.\n\n"
            "Exhibitor at AIPAD, Armory, Art Miami, Paris Photo, PULSE and Scope."
        ),
        "website": "http://www.yanceyrichardson.com/",
        "phone": "+1 646 230 9610",
        "phone2": "",
        "image_link": "/cloud/website-images/Yancey-Richardson-Gallery.jpg",
        "image_alt": "Yancey Richardson Gallery",
        "sortorder": 40,
    },
]


class Command(BaseCommand):
    help = "Seed the Galleries table from the known list of representing galleries."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing Gallery rows before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            count, _ = Gallery.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {count} existing gallery rows."))

        created_count = 0
        updated_count = 0

        for data in SEED_DATA:
            # Resolve / create Country
            country, c_created = Country.objects.get_or_create(label=data["country"])
            if c_created:
                self.stdout.write(f"  Created country: {country}")

            # Resolve / create Place
            place, p_created = Place.objects.get_or_create(
                label=data["city"],
                country=country,
            )
            if p_created:
                self.stdout.write(f"  Created place: {place}")

            # Upsert Gallery
            gallery, g_created = Gallery.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "name": data["name"],
                    "place": place,
                    "description": data["description"],
                    "website": data["website"],
                    "phone": data["phone"],
                    "phone2": data["phone2"],
                    "image_link": data["image_link"],
                    "image_alt": data["image_alt"],
                    "sortorder": data["sortorder"],
                },
            )
            if g_created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  Created: {gallery}"))
            else:
                updated_count += 1
                self.stdout.write(f"  Updated: {gallery}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone — {created_count} created, {updated_count} updated."
            )
        )
