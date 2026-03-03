"""
Create the PublicationMedia table directly with raw SQL.

Needed because Photos.Id is int in SQL Server but Django's DEFAULT_AUTO_FIELD
(BigAutoField) would generate a bigint FK column, causing a type mismatch error
on the FK constraint. This command mirrors the ExhibitionMedia table structure.

Usage:
    python manage.py create_publication_media_table
"""

from django.core.management.base import BaseCommand
from django.db import connection


CREATE_SQL = """
IF NOT EXISTS (
    SELECT 1 FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_NAME = 'PublicationMedia'
)
BEGIN
    CREATE TABLE [dbo].[PublicationMedia] (
        [id]            bigint IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [PublicationId] bigint NOT NULL,
        [MediumId]      int    NULL,
        [MediumType]    nvarchar(100)  NOT NULL DEFAULT '',
        [Caption]       nvarchar(500)  NOT NULL DEFAULT '',
        [Indexed]       bit            NULL,
        [Sortorder]     bigint         NULL,
        CONSTRAINT [PublicationMedia_PublicationId_fk]
            FOREIGN KEY ([PublicationId])
            REFERENCES [dbo].[Publications] ([id]),
        CONSTRAINT [PublicationMedia_MediumId_fk]
            FOREIGN KEY ([MediumId])
            REFERENCES [dbo].[Photos] ([Id])
    );
    PRINT 'PublicationMedia table created.';
END
ELSE
BEGIN
    PRINT 'PublicationMedia table already exists — skipped.';
END
"""


class Command(BaseCommand):
    help = "Create the PublicationMedia table in SQL Server using raw DDL."

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(CREATE_SQL)
        self.stdout.write(self.style.SUCCESS("Done."))
