from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Inspect tables and FK relationships in the DB"

    def handle(self, *args, **options):
        with connection.cursor() as cur:
            self.stdout.write("=== Media columns ===")
            cur.execute("""
                SELECT c.COLUMN_NAME, c.DATA_TYPE, c.CHARACTER_MAXIMUM_LENGTH,
                       c.IS_NULLABLE, c.COLUMN_DEFAULT
                FROM INFORMATION_SCHEMA.COLUMNS c
                WHERE c.TABLE_NAME = 'Media'
                ORDER BY c.ORDINAL_POSITION
            """)
            for row in cur.fetchall():
                self.stdout.write(str(row))

            self.stdout.write("\n=== Media FKs ===")
            cur.execute("""
                SELECT fk.name, cp.name AS col, tr.name AS ref_table, cr.name AS ref_col
                FROM sys.foreign_keys fk
                JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
                JOIN sys.tables tp  ON fkc.parent_object_id = tp.object_id
                JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id
                                   AND fkc.parent_column_id = cp.column_id
                JOIN sys.tables tr  ON fkc.referenced_object_id = tr.object_id
                JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id
                                   AND fkc.referenced_column_id = cr.column_id
                WHERE tp.name = 'Media'
            """)
            for row in cur.fetchall():
                self.stdout.write(str(row))
