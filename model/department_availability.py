from pymodm import MongoModel, fields


class DepartmentAvailability(MongoModel):
    departmentCode = fields.CharField(primary_key=True)
    departmentName = fields.CharField()
    bookingOpen = fields.BooleanField()
    bookingFirstOpenSlotDate = fields.DateTimeField(blank=True)
    departmentBookUrl = fields.CharField(blank=True)
