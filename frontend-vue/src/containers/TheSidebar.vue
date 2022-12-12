<template>
  <CSidebar
    fixed
    :minimize="minimize"
    :show="show"
    @update:show="(value) => $store.commit('set', ['sidebarShow', value])"
    class="sidebar-bg"
    width="304"
  >
    <CSidebarBrand class="d-md-down-none">
       <div class="kaist-log"> </div>
    </CSidebarBrand>
    <CRenderFunction v-if="$session.getUserType() == 1" flat :content-to-render="$options.nav"/>
    <CRenderFunction v-else flat :content-to-render="$options.nav_anyone"/>
  </CSidebar>
</template>

<script>
import nav from './_nav'
import nav_anyone from './_nav_anyone'
import { brandSet as brands } from '@coreui/icons'
export default {
  name: 'TheSidebar',
  nav,
  nav_anyone,
  brands,
  computed: {
    show () {
      return this.$store.state.sidebarShow 
    },
    minimize () {
      return this.$store.state.sidebarMinimize 
    }
  },
  methods:{
    move_first() {
      if(this.$session.check_permission()){
        this.$session.logout()
        this.$router.push('/login').catch(()=>{});
      }else{
        this.$router.push('/login').catch(()=>{});
        location.reload(true)
      }

    }

  }

}
</script>
<style scoped lang="scss">
.cb-log{
  font-size: 20px;
  font-weight: bold;
  margin-left: 10px;
}
.sidebar-bg{
  background-image: url('~@/assets/bg/left-bg.png');
}
.kaist-log{
  background-image: url('~@/assets/bg/kaist-logo.png');
  background-size: 100px;
  position: absolute;
  left: 0.36%;
  right: 0.36%;
  top: 1.27%;
  bottom: 1.26%;
}
</style>
