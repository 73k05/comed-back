from datetime import datetime

from pymodm import MongoModel, fields


class DepartmentAvailability(MongoModel):
    departmentCode = fields.CharField(primary_key=True)
    departmentName = fields.CharField()
    bookingOpen = fields.BooleanField()
    bookingFirstOpenSlotDate = fields.DateTimeField(blank=True)
    departmentBookUrl = fields.CharField(blank=True)
    createDate = fields.DateTimeField()
    updateDate = fields.DateTimeField()

    def save(self):
        self.updateDate = datetime.now()
        if not self.createDate:
            self.createDate = datetime.now()
        super(DepartmentAvailability, self).save()
