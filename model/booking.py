from datetime import datetime

from pymodm import fields, MongoModel


class Booking(MongoModel):
    email = fields.EmailField()
    firstName = fields.CharField()
    lastName = fields.CharField()
    phone = fields.CharField()
    number = fields.IntegerField()
    birthDate = fields.DateTimeField()
    birthName = fields.CharField(blank=True)
    region = fields.CharField()
    typeVisit = fields.CharField()
    bookingChooseDate = fields.DateTimeField()
    bookedCurrentDate = fields.DateTimeField(blank=True)
    addressStreet = fields.CharField()
    addressZip = fields.CharField()
    addressCity = fields.CharField()
    departmentName = fields.CharField()
    departmentCode = fields.CharField()
    bookUrl = fields.CharField()
    endPointUrl = fields.CharField()
    indexDayZero = fields.IntegerField()
    archived = fields.BooleanField()
    createDate = fields.DateTimeField()
    updateDate = fields.DateTimeField()

    def save(self):
        self.updateDate = datetime.now()
        if not self.createDate:
            self.createDate = datetime.now()
        super(Booking, self).save()
