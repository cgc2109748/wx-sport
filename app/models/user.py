from mongoengine import Document, StringField, IntField, BooleanField,ListField

class User(Document):
    openid = StringField(required=True)
    nickName = StringField()
    avatarUrl = StringField()
    city = StringField()
    country = StringField()
    gender = IntField()
    is_demote = BooleanField()
    language = StringField()
    province = StringField()
    integral = IntField(default=0)
    signInRecords = ListField(StringField())