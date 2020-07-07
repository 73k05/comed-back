from pymodm import MongoModel, fields


class DepartmentAvailability(MongoModel):
    departmentCode = fields.CharField()
    departmentName = fields.CharField()
    bookingOpen = fields.BooleanField()
    bookingFirstOpenSlotDate = fields.DateTimeField()
    departmentBookUrl = fields.CharField()
