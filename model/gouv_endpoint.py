from datetime import datetime

from pymodm import MongoModel, fields


class GouvEndPoint(MongoModel):
    departmentCode = fields.CharField(primary_key=True)
    departmentName = fields.CharField()
    bypass = fields.BooleanField()
    endPointUrl = fields.CharField(blank=True)
    indexDayZero = fields.IntegerField()
    bookUrl = fields.CharField(blank=True)
    createDate = fields.DateTimeField()
    updateDate = fields.DateTimeField()

    def save(self):
        self.updateDate = datetime.now()
        if not self.createDate:
            self.createDate = datetime.now()
        super(GouvEndPoint, self).save()
