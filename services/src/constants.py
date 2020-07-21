# File to hold constants
from builtins import Exception

saasUserManTenant="linkvis"
jwtHeaderName="jwt-auth-token"
jwtCookieName="jwt-auth-token"
loginCookieName="usersystemUserCredentials"

DefaultHasAccountRole="hasaccount"
SecurityEndpointAccessRole="securityTest"

incorrectAccessLevelResponse = "Incorrect Access Level for this graph"
incorrectAccessToTargetResponse = "Incorrect Access Level to target namespace"


class customExceptionClass(Exception):
  id = None
  text = None
  def __init__(self, text, iid=None):
    if iid is None:
      self.id = text
    else:
      self.id = iid
    self.text = text
