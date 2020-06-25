import datetime

from peewee import (
    SqliteDatabase,
    Model, AutoField, CharField, DateTimeField
)

db = SqliteDatabase('DCTCS.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = AutoField()  # User.id will be auto-incrementing PK.
    name = CharField(unique=False)
    checkin_time = DateTimeField(default=datetime.datetime.now)


class Room(BaseModel):
    id = AutoField()
