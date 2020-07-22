// This file is for calling my backend services
import rjmversion from './rjmversion.js'

var endpointName = 'saas_challengeapp'
function getMainEndpointName () {
  return endpointName
}

// var authedStoreFn = 'saasUserManagementClientStore/callAuthedAPI'
// var authedOrAnonStoreFn = 'saasUserManagementClientStore/callAuthedOrAnonAPI'

// Change this variable to use different major bersions of login service
var prodLoginServiceBaseURL = 'https://api.metcarob.com/saas_user_management/v0/'

var prodLoginTenantName = 'challengeapp' // Configured login tenant on prod
var loaclDevLoginTenantName = 'challengeappDEV' // Should match value in /services/_start_local_saas_user_management_service_config.json

function finishEndPointIdentificationHook (stores, { serverInfo, apiPrefix }) {
  // Do nothing
}

function registerEndpoints (stores, prodDomain, runtype) {
  var finishEndPointIdentificationHookFN = function (params) {
    finishEndPointIdentificationHook(stores, params)
  }
  if (stores.getters['saasUserManagementClientStore/isLogginProcessStateRegistered']) {
    return
  }
  if (runtype === 'proddomain') {
    var majorCodeVersion = rjmversion.codebasever.split('.')[0]
    console.log('PROD taking api version from code', runtype, majorCodeVersion)
    stores.dispatch('saasUserManagementClientStore/registerLoginEndpoint', {
      loginServiceBaseURL: prodLoginServiceBaseURL,
      loginTenantName: prodLoginTenantName
    })

    // https://api.metcarob.com/saas_linkvis/v0
    var possibleApiPrefixes = [{ prefix: 'https://api.metcarob.com/' + endpointName + '/v' + majorCodeVersion, connectingthroughnginx: true, apitype: 'public' }]
    stores.dispatch('saasUserManagementClientStore/registerEndpoint', {
      endpoint: endpointName,
      apiPrefixIdentificationProcessConfig: {
        possibleApiPrefixes: possibleApiPrefixes
      },
      finishEndPointIdentificationHook: finishEndPointIdentificationHookFN
    })
  } else {
    var prodVer = stores.getters['saasUserManagementClientStore/getProdVerFn'](window.location.href, endpointName)
    if (prodVer.prod) {
      console.log('PROD taking api version from url ', runtype)
      stores.dispatch('saasUserManagementClientStore/registerLoginEndpoint', {
        loginServiceBaseURL: prodLoginServiceBaseURL,
        loginTenantName: prodLoginTenantName
      })

      var possibleApiPrefixes2 = [{ prefix: prodVer.prefix, connectingthroughnginx: true, apitype: 'public' }]
      stores.dispatch('saasUserManagementClientStore/registerEndpoint', {
        endpoint: endpointName,
        apiPrefixIdentificationProcessConfig: {
          possibleApiPrefixes: possibleApiPrefixes2
        },
        finishEndPointIdentificationHook: finishEndPointIdentificationHookFN
      })
    } else {
      console.log('NON PROD no api version needed using same basepath', runtype)
      stores.dispatch('saasUserManagementClientStore/registerLoginEndpoint', {
        loginServiceBaseURL: 'http://127.0.0.1:8099/',
        loginTenantName: loaclDevLoginTenantName
      })

      stores.dispatch('saasUserManagementClientStore/registerEndpoint', {
        endpoint: endpointName,
        apiPrefixIdentificationProcessConfig: {
          possibleApiPrefixes: [{ prefix: 'http://localhost:8098', connectingthroughnginx: false, apitype: 'public' }]
        },
        finishEndPointIdentificationHook: finishEndPointIdentificationHookFN
      })
    }
  }

  var requestUserReloginINT = function (message, curpath) {
    requestUserRelogin(message, curpath, stores)
  }
  stores.commit('saasUserManagementClientStore/REGISTERREQUESTUSERRELOGINFN', { requestUserReloginFn: requestUserReloginINT })

  var callback = {
    ok: function ({ serverinfoResponse, endpoint, sucessfulapiprefix }) {
    },
    error: function (response) {
    }
  }
  stores.dispatch('saasUserManagementClientStore/startEndpointIdentificationProcessAction', {
    endpoint: endpointName,
    callback: callback
  })
}

function requestUserRelogin (message, curpath, stores) {
  var thisQuasarPath = curpath
  var returnAddress = window.location.protocol + '//' + window.location.host + window.location.pathname + '#' + thisQuasarPath
  if (returnAddress.includes('saas_user_management')) {
    console.log('requestUserRelogin: error, found that returnAddress includes saas_user_management')
    console.log('window.location.protocol', window.location.protocol)
    console.log('window.location.host', window.location.host)
    console.log('window.location.pathname', window.location.pathname)
    console.log('thisQuasarPath', thisQuasarPath)
    console.log('Did not preform redirect to:', stores.getters['saasUserManagementClientStore/getLoginUIURLFn'](message, '/', returnAddress))
  } else {
    window.location.href = stores.getters['saasUserManagementClientStore/getLoginUIURLFn'](message, '/', returnAddress)
  }
}

export default {
  registerEndpoints: registerEndpoints,
  // callUInfoAPI: callUInfoAPI,
  // callExploreAPI: callExploreAPI,
  // callCreateAPI: callCreateAPI,
  // callDesignAPI: callDesignAPI,
  getMainEndpointName: getMainEndpointName
}
