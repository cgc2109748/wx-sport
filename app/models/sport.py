from mongoengine import Document, StringField

class Sport(Document):
    title = StringField(required=True)
    organizer = StringField(required=True)
    tags = StringField()
    startDate = StringField(required=True)
    startTime = StringField(required=True)
    endDate = StringField(required=True)
    endTime = StringField(required=True)
    content = StringField()
    image = StringField()  
    status = StringField(default='pending')
    createdAt = StringField()
