from datetime import datetime

from pymodm import fields, MongoModel
from pymodm.errors import ValidationError

from utils.log import write_log


class Booking(MongoModel):
    email = fields.EmailField()
    firstName = fields.CharField()
    lastName = fields.CharField()
    phone = fields.CharField(blank=True)
    number = fields.IntegerField()
    birthDate = fields.DateTimeField(blank=True)
    birthName = fields.CharField(blank=True)
    region = fields.CharField(blank=True)
    typeVisit = fields.CharField(blank=True)
    bookingChooseDate = fields.DateTimeField()
    bookedCurrentDate = fields.DateTimeField(blank=True)
    addressStreet = fields.CharField(blank=True)
    addressZip = fields.CharField(blank=True)
    addressCity = fields.CharField(blank=True)
    departmentName = fields.CharField()
    departmentCode = fields.CharField(blank=True)
    bookUrl = fields.CharField(blank=True)
    endPointUrl = fields.CharField(blank=True)
    indexDayZero = fields.IntegerField()
    premiumBooking = fields.BooleanField(blank=True)
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
