from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern


class GouvEndPoint(MongoModel):
    departmentCode = fields.CharField(primary_key=True)
    departmentName = fields.CharField()
    bypass = fields.BooleanField()
    endPointUrl = fields.CharField(blank=True)
    indexDayZero = fields.IntegerField()
    bookUrl = fields.CharField(blank=True)

    # class Meta:
    #     write_concern = WriteConcern(j=True)
    #     connection_alias = 'my-app'
