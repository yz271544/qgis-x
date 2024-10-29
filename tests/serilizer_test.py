#!/usr/bin/env python 
# -*- encoding: utf-8 -*- 
# Project: spd-sxmcc 
"""
@file: serilizer_test.py
@author: Lyndon
@time: 2024/10/29 12:13
@env: Python @desc:
@ref: @blog:
"""

import json
import unittest

class SerilizerTest(unittest.TestCase):

    data_resp = r"""{
  "createBy": "jingwei",
  "createTime": "2024-10-24 04:55:10",
  "updateBy": "jingwei",
  "updateTime": "2024-10-24 04:55:10",
  "remark": null,
  "id": "1849313659602386946",
  "sceneId": "1847168269595754497",
  "plottingType": 0,
  "coverageId": "6e016fe4-f18c-11ee-bfc1-fa163ebdd4f8",
  "coverageCode": "0105",
  "basicsPropertiesJson": "{\"name\":\"李四\",\"tel\":\"13933331112\",\"showTel\":false,\"company\":\"郑州市公安局特勤局\",\"lead\":\"\",\"leadTel\":\"\",\"remark\":\"\",\"lngLatAlt\":\"\",\"longitude\":111.485056,\"latitude\":40.727639,\"type\":\"201\",\"typeName\":\"执勤人员\",\"code\":\"0105\",\"layName\":\"民警\",\"nature\":\"\",\"carCode\":\"\",\"size\":\"\",\"position\":\"\",\"long\":0,\"width\":0,\"sex\":\"0\",\"nation\":\"汉族\",\"nativePlace\":\"\",\"birthTime\":\"1981-02\",\"politicsStatus\":\"01\",\"educationBackground\":\"06\",\"jobResume\":\"\",\"policeDeptOpinion\":\"\",\"card\":\"\",\"drivingType\":\"\",\"drivingAge\":\"\",\"heathCondition\":\"\",\"post\":\"12\",\"prop1\":\"\",\"prop2\":\"\",\"prop3\":\"\",\"prop4\":\"\",\"prop5\":\"\",\"prop6\":\"\",\"prop7\":\"\",\"line\":\"\",\"dept1\":\"\",\"person1\":\"\",\"tel1\":\"\",\"dept2\":\"\",\"person2\":\"\",\"tel2\":\"\",\"dept3\":\"\",\"person3\":\"\",\"tel3\":\"\",\"dept4\":\"\",\"person4\":\"\",\"tel4\":\"\",\"description\":\"\",\"range\":\"\",\"personNum\":\"\",\"totalLevelNum\":\"\",\"viewLevelNum\":\"\",\"viewWindowNum\":\"\",\"ageName\":\"\",\"heightName\":\"\",\"physicalResult\":\"01\",\"physicalResultName\":\"健康\",\"psychologicalResult\":\"01\",\"psychologicalResultName\":\"积极\",\"jobCount\":10,\"dept\":\"\",\"serviceCondition\":\"\",\"sexName\":\"男\",\"educationBackgroundName\":\"本科\",\"postName\":\"民警\",\"politicsStatusName\":\"中共党员\",\"duty\":\"\",\"nationality\":\"\",\"address\":\"\",\"star\":\"\",\"area\":\"\",\"build\":\"\",\"floor\":\"\",\"room\":\"\",\"workers\":\"\",\"foreigns\":\"\",\"regions\":\"\",\"card1\":\"\",\"card2\":\"\"}",
  "extendPropertiesJson": "[{\"label\":\"\",\"val\":\"\"}]",
  "name": "李四",
  "licensePlateNumber": null,
  "longitudeLatitude": "{\"type\":\"Feature\",\"geometry\":{\"type\":\"Point\",\"coordinates\":[111.485056,40.727639]},\"properties\":{}}",
  "shape": "{\"type\":\"Feature\",\"geometry\":{\"type\":\"Point\",\"coordinates\":[111.485056,40.727639,1023.411652]},\"properties\":{}}",
  "styleFlag": 0,
  "styleInfoJson": "{\"color\":\"rgba(255,255,255,1)\",\"bim\":\"\",\"num\":2,\"loadFlag\":false,\"fontStyle\":{\"borderColor\":\"rgba(255,255,255,1)\",\"loadFlag\":true,\"x\":0,\"y\":35,\"fontSize\":20,\"fontColor\":\"rgba(0, 50, 230, 1)\",\"fontFlag\":false},\"type\":\"01\",\"originLoadFlag\":true,\"radius\":100}",
  "realityImagesOne": "[\"\"]",
  "realityImagesTwo": "[]",
  "rangeImages": "[]",
  "delFlag": false,
  "watchPerson": "[]",
  "watchPersonInfo": [],
  "coverageCodes": null,
  "plottingTypeQuery": null,
  "plottingTypes": null
}"""

    def test_deserialize_json(self):
        # data_resp = self.data_resp.decode('utf-8')
        # data_resp = json.loads(data_resp)
        data_resp = json.loads(self.data_resp)
        print(data_resp)
        print(data_resp["basicsPropertiesJson"])
        basicsPropertiesJson = json.loads(data_resp['basicsPropertiesJson'])
        print(basicsPropertiesJson)
