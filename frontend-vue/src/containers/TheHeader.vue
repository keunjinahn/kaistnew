<template>
  <CHeader fixed with-subheader light>

    <CToggler
      in-header
      class="ml-3 d-lg-none"
      @click="$store.commit('toggleSidebarMobile')"
    />
    <CToggler
      in-header
      class="ml-3 d-md-down-none"
      @click="$store.commit('toggleSidebarDesktop')"
    />
<!--    <CHeaderBrand class="mx-auto d-lg-none" to="/">-->
<!--      <CIcon name="logo" height="48" alt="Logo"/>-->
<!--    </CHeaderBrand>-->
    <CHeaderNav class="d-md-down-none mr-auto">
<!--      <CHeaderNavItem class="px-3">-->
<!--        <CHeaderNavLink to="/dashboard">-->
<!--          대시보드-->
<!--        </CHeaderNavLink>-->
<!--      </CHeaderNavItem>-->
<!--      <CHeaderNavItem class="px-3">-->
<!--        <CHeaderNavLink to="/users" exact>-->
<!--          사용자-->
<!--        </CHeaderNavLink>-->
<!--      </CHeaderNavItem>-->
<!--      <CHeaderNavItem class="px-3">-->
<!--        <CHeaderNavLink>-->
<!--          설정-->
<!--        </CHeaderNavLink>-->
<!--      </CHeaderNavItem>-->
    </CHeaderNav>
    <CHeaderNav v-if="$session.authorized" class="mr-4">
<!--      <CHeaderNavItem class="d-md-down-none mx-2">-->
<!--        <CHeaderNavLink>-->
<!--          <CIcon name="cil-bell"/>-->
<!--        </CHeaderNavLink>-->
<!--      </CHeaderNavItem>-->
<!--      <CHeaderNavItem class="d-md-down-none mx-2">-->
<!--        <CHeaderNavLink>-->
<!--          <CIcon name="cil-list"/>-->
<!--        </CHeaderNavLink>-->
<!--      </CHeaderNavItem>-->
<!--      <CHeaderNavItem class="d-md-down-none mx-2">-->
<!--        <CHeaderNavLink>-->
<!--          <CIcon name="cil-envelope-open"/>-->
<!--        </CHeaderNavLink>-->
<!--      </CHeaderNavItem>-->
      <TheHeaderDropdownAccnt/>
    </CHeaderNav>
    <CHeaderNav v-else class="px-3">
      <v-icon big @click="move_first()">mdi-application-import</v-icon>나가기
    </CHeaderNav>
<!--    <CSubheader class="px-3">-->
<!--      <CBreadcrumbRouter class="border-0 mb-0"/>-->
<!--    </CSubheader>-->
  </CHeader>
</template>

<script>
import TheHeaderDropdownAccnt from './TheHeaderDropdownAccnt'

export default {
  name: 'TheHeader',
  components: {
    TheHeaderDropdownAccnt
  },
  methods:{
    move_first(){
      location.reload(true)
    }
  }
}
</script>
<style scoped>
.m-t{
  margin-top: 15px;
}
</style>
