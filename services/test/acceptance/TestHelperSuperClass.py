import unittest
import pytz
import datetime
from appObj import appObj
import json
import constants
import TestingHelper
from unittest.mock import patch
import copy
import uuid

import logging

from nose.plugins.attrib import attr
def wipd(f):
    return attr('wip')(f)

from SessionMock import SessionMock

import python_Testing_Utilities


httpOrigin = 'http://a.com'

infoAPIPrefix = '/api/public/info'

env = {
  'APIAPP_MODE': 'DOCKER',
  'APIAPP_JWTSECRET': 'DOsaddsaCKER',
  'APIAPP_VERSION': 'TEST-3.3.3',
  'APIAPP_FRONTEND': '_',
  'APIAPP_APIURL': 'http://apiurlxxx',
  'APIAPP_FRONTENDURL': 'http://frontenddummytestxxx',
  'APIAPP_APIACCESSSECURITY': '[]',
  'APIAPP_COMMON_ACCESSCONTROLALLOWORIGIN': httpOrigin + ', https://sillysite.com',
}


class testClassWithTestClient(unittest.TestCase):
  testClient = None
  standardStartupTime = pytz.timezone('Europe/London').localize(datetime.datetime(2018,1,1,13,46,0,0))

  def _getEnvironment(self):
    raise Exception("Should be overridden")

  def setUp(self):
    self.pre_setUpHook()
    appObj.init(self._getEnvironment(), self.standardStartupTime, testingMode=True)
    self.testClient = appObj.flaskAppObject.test_client()
    self.testClient.testing = True

  def tearDown(self):
    self.testClient = None

  def pre_setUpHook(self):
    pass


ownerUserID = '3efv'
securityEndpointCredentials = {
  "userID": 'admin',
  "roles": [ constants.DefaultHasAccountRole, constants.SecurityEndpointAccessRole ]
}
normalUser1ID = 'reg3rf'
normalUser2ID = 'reg3gf'

class testClassWithHelpers(testClassWithTestClient):

  # acceptedResultList can be none then never assert
  def assertAPIResult(self, methodFN, url, session, data, acceptedResultList, msg):
    headers = None
    if session != None:
      headers = {
        constants.jwtHeaderName: SessionMock.from_Session(session).getJWTToken()
      }
    if methodFN.__name__ == 'get':
      if data != None:
        raise Exception("Trying to send post data to a get request")
    result = methodFN(
      url,
      headers=headers,
      data=json.dumps(data),
      content_type='application/json'
    )
    if acceptedResultList != None:
      if result.status_code not in acceptedResultList:
        self.assertTrue(False, msg="calling " + url + "(" + methodFN.__name__ + ") - Expected one of " + str(acceptedResultList) + " got " + str(result.status_code) + "  " + result.get_data(as_text=True))
    try:
      resultJSON = json.loads(result.get_data(as_text=True))
    except:
      self.assertTrue(False, msg="API response not JSON - " + result.get_data(as_text=True))
    return resultJSON

  def assertInfoAPIResult(self, methodFN, url, session, data, acceptedResultList, msg):
    return self.assertAPIResult(methodFN, infoAPIPrefix + url, session, data, acceptedResultList, msg)

  def login(self, credentials):
    return SessionMock.from_Credentials(credentials).getSession()

