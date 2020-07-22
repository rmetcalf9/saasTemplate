// This file is for calling my backend services

var endpointName = 'saas_challengeapp'
function getMainEndpointName () {
  return endpointName
}

export default {
  // registerEndpoints: registerEndpoints,
  // callUInfoAPI: callUInfoAPI,
  // callExploreAPI: callExploreAPI,
  // callCreateAPI: callCreateAPI,
  // callDesignAPI: callDesignAPI,
  getMainEndpointName: getMainEndpointName
}
