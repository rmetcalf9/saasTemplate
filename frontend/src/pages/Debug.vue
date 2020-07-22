<template>
  <q-page class="flex flex-center">
    <q-list bordered padding>
      <q-item>
        <q-item-label header>Debug Information and functions</q-item-label>
      </q-item>
      <q-item>
         <q-item-section>
         <q-item-label>Make browser clear all caches for this app</q-item-label>
         <q-btn color="primary" label="Force Reload"
                   @click="forcereload" >
        </q-btn>
         </q-item-section>
       </q-item>
       <q-item>
         <q-item-section>
          Debug Stats
          <q-item-label caption>{{ debugStats }}</q-item-label>
         </q-item-section>
       </q-item>
       <q-item>
         <q-btn color="primary" @click="btnBack">Back to main page</q-btn>
       </q-item>

     </q-list>

  </q-page>
</template>

<style>
</style>

<script>

export default {
  name: 'DebugInformation',
  data () {
    return {
    }
  },
  methods: {
    forcereload () {
      // Clear all caches - https://stackoverflow.com/questions/54376355/clear-workbox-cache-of-all-content
      caches.keys().then(cacheNames => {
        cacheNames.forEach(cacheName => {
          caches.delete(cacheName)
        })
      })
      window.location.reload(true)
    },
    btnBack () {
      try {
        this.$router.replace('/').catch((myerr) => {
          // console.log('Error going back 2', myerr)
          //  Ignoring this error
        })
      } catch {
        console.log('Error going back')
      }
    }
  },
  computed: {
    debugStats () {
      return this.$store.getters['saasUserManagementClientStore/getDebugStats']
    }
  }
}
</script>
