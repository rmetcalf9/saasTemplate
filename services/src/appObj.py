#appObj.py - This file contains the main application object
# to be constructed by app.py

from baseapp_for_restapi_backend_with_swagger import AppObjBaseClass as parAppObj, readFromEnviroment

import constants
from object_store_abstraction import createObjectStoreInstance
import uuid
import json

import logging
import sys


#API's
##from APIadmin import registerAPI as registerAdminApi

invalidConfigurationException = constants.customExceptionClass('Invalid Configuration')

InvalidObjectStoreConfigInvalidJSONException = constants.customExceptionClass('APIAPP_OBJECTSTORECONFIG value is not valid JSON')
InvalidChartStoreConfigInvalidJSONException = constants.customExceptionClass('APIAPP_CHARTSTORECONFIG value is not valid JSON')


class appObjClass(parAppObj):
  objectStore = None
  APIAPP_OBJECTSTOREDETAILLOGGING = None
  accessControlAllowOriginObj = None
  operationsLogic = None
  chartStoreConnectionRepository = None

  def setupLogging(self):
    root = logging.getLogger()
    #root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

  def init(self, env, serverStartTime, testingMode = False):
    ##self.setupLogging() Comment in when debugging

    super(appObjClass, self).init(env, serverStartTime, testingMode, serverinfoapiprefix='public/info')

    #This app always needs a JWT key
    if self.APIAPP_JWTSECRET is None:
      print("ERROR - APIAPP_JWTSECRET should always be set")
      raise invalidConfigurationException

    objectStoreConfigJSON = readFromEnviroment(env, 'APIAPP_OBJECTSTORECONFIG', '{}', None)
    objectStoreConfigDict = None
    try:
      if objectStoreConfigJSON != '{}':
        objectStoreConfigDict = json.loads(objectStoreConfigJSON)
    except Exception as err:
      print(err) # for the repr
      print(str(err)) # for just the message
      print(err.args) # the arguments that the exception has been called with.
      raise(InvalidObjectStoreConfigInvalidJSONException)

    self.APIAPP_OBJECTSTOREDETAILLOGGING = readFromEnviroment(
      env=env,
      envVarName='APIAPP_OBJECTSTOREDETAILLOGGING',
      defaultValue='N',
      acceptableValues=['Y', 'N'],
      nullValueAllowed=True
    ).strip()
    if (self.APIAPP_OBJECTSTOREDETAILLOGGING=='Y'):
      print("APIAPP_OBJECTSTOREDETAILLOGGING set to Y - statement logging enabled")

    fns = {
      'getCurDateTime': self.getCurDateTime
    }
    self.objectStore = createObjectStoreInstance(
      objectStoreConfigDict,
      fns,
      detailLogging=(self.APIAPP_OBJECTSTOREDETAILLOGGING=='Y')
    )


  def initOnce(self):
    super(appObjClass, self).initOnce()
    ##registerAdminApi(self)

    self.flastRestPlusAPIObject.title = "Challange App"
    self.flastRestPlusAPIObject.description = "API for Challange App"

  def stopThread(self):
    ##print("stopThread Called")
    pass

  #override exit gracefully to stop worker thread
  def exit_gracefully(self, signum, frame):
    self.stopThread()
    super(appObjClass, self).exit_gracefully(signum, frame)

  def getDerivedServerInfoData(self):
    return {
      ##"APIAPP_LINKVISCONNECTORBASEURL": self.APIAPP_LINKVISCONNECTORBASEURL
    }

appObj = appObjClass()
