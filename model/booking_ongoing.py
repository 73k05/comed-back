from pymodm import MongoModel, fields


class BookingOngoing(MongoModel):
    email = fields.EmailField(primary_key=True)
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
    indexDayZero = fields.CharField()
