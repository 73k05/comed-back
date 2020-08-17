from datetime import datetime

from pymodm import fields, MongoModel
from pymodm.errors import ValidationError

from utils.log import write_log


class Booking(MongoModel):
    email = fields.EmailField()
    firstName = fields.CharField()
    lastName = fields.CharField()
    phone = fields.CharField()
    number = fields.IntegerField()
    birthDate = fields.DateTimeField()
    birthName = fields.CharField(blank=True)
    region = fields.CharField(blank=True)
    typeVisit = fields.CharField()
    bookingChooseDate = fields.DateTimeField()
    bookedCurrentDate = fields.DateTimeField(blank=True)
    addressStreet = fields.CharField()
    addressZip = fields.CharField()
    addressCity = fields.CharField()
    departmentName = fields.CharField()
    departmentCode = fields.CharField(blank=True)
    bookUrl = fields.CharField(blank=True)
    endPointUrl = fields.CharField(blank=True)
    indexDayZero = fields.IntegerField()
    archived = fields.BooleanField()
    createDate = fields.DateTimeField()
    updateDate = fields.DateTimeField()

    def save(self):
        self.updateDate = datetime.now()
        if not self.createDate:
            self.createDate = datetime.now()
        try:
            super(Booking, self).save()
        except ValidationError as e:
            write_log(f"Error saving booking: {e}")
