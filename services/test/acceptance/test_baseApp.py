# simple test to make sure baseapp is properly configured

import TestHelperSuperClass
import python_Testing_Utilities

class helpers(TestHelperSuperClass.testClassWithHelpers):
  def _getEnvironment(self):
    return TestHelperSuperClass.env

class test_adminapi(helpers):
  def test_infoEndpoint(self):
    #call rsults as /api/public/info/serverinfo
    apiResult = self.assertInfoAPIResult(
      methodFN=self.testClient.get,
      url="/serverinfo",
      session=None,
      data=None,
      acceptedResultList=[200],
      msg="Create user call returned error"
    )
    expectedRes = {
      'Server': {
        'APIAPP_APIDOCSURL': '_',
        'Version': 'TEST-3.3.3',
        'APIAPP_FRONTENDURL': TestHelperSuperClass.env['APIAPP_FRONTENDURL']
      },
      'Derived': {
        #'APIAPP_LINKVISCONNECTORBASEURL': TestHelperSuperClass.env['APIAPP_LINKVISCONNECTORBASEURL']
      }
    }

    python_Testing_Utilities.assertObjectsEqual(
      unittestTestCaseClass=self,
      first=apiResult,
      second=expectedRes,
      msg="Server Info return wrong",
      ignoredRootKeys=[]
    )
