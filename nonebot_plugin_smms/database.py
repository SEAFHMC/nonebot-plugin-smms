from pathlib import Path
from os import path
import peewee as pw

db_path = Path().absolute() / "data" / "smms" / "data.db"
db_path.parent.mkdir(exist_ok=True, parents=True)
db = pw.SqliteDatabase(db_path)


class ImageTable(pw.Model):
    user_id = pw.IntegerField()
    tag = pw.CharField()
    store_name = pw.CharField()
    img_url = pw.CharField()
    delete_url = pw.CharField()

    class Meta:
        database = db
        primary_key = pw.CompositeKey(
            "user_id", "tag", "store_name", "img_url", "delete_url"
        )


if not path.exists(db_path):
    db.connect()
    db.create_tables([ImageTable])
    db.close()
