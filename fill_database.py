from pymodm.connection import connect
from model.gouv_endpoint import GouvEndPoint
import json

connect("mongodb://localhost:27017/comed")

with open('json/gouvendpoints.json') as json_data:
    url_department_list = json.load(json_data)["gouvUrlList"]

department_availability_list = []

# Creates gouv endpoint in db
for department in url_department_list:
    gouv_endpoint = GouvEndPoint(department["departmentCode"], department["departmentName"],
                                 department["bypass"], department["endPointUrl"],
                                 department["indexDayZero"], department["bookUrl"])
    gouv_endpoint.save()
