<template>
  <CDropdown
    inNav
    class="c-header-nav-items"
    placement="bottom-end"
    add-menu-classes="pt-0"
  >
    <template #toggler>
      <CHeaderNavLink>
        <div class="logout-size">
          <v-icon big>mdi-application-import</v-icon>
          로그아웃
        </div>
      </CHeaderNavLink>
    </template>
<!--    <CDropdownHeader tag="div" class="text-center" color="light">-->
<!--      <strong>Account</strong>-->
<!--    </CDropdownHeader>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-bell"/> Updates-->
<!--      <CBadge color="info" class="mfs-auto">{{ itemsCount }}</CBadge>-->
<!--    </CDropdownItem>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-envelope-open" /> Messages-->
<!--      <CBadge color="success" class="mfs-auto">{{ itemsCount }}</CBadge>-->
<!--    </CDropdownItem>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-task" /> Tasks-->
<!--      <CBadge color="danger" class="mfs-auto">{{ itemsCount }}</CBadge>-->
<!--    </CDropdownItem>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-comment-square" /> Comments-->
<!--      <CBadge color="warning" class="mfs-auto">{{ itemsCount }}</CBadge>-->
<!--    </CDropdownItem>-->
<!--    <CDropdownHeader-->
<!--      tag="div"-->
<!--      class="text-center"-->
<!--      color="light"-->
<!--    >-->
<!--      <strong>Settings</strong>-->
<!--    </CDropdownHeader>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-user" /> Profile-->
<!--    </CDropdownItem>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-settings" /> Settings-->
<!--    </CDropdownItem>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-dollar" /> Payments-->
<!--      <CBadge color="secondary" class="mfs-auto">{{ itemsCount }}</CBadge>-->
<!--    </CDropdownItem>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-file" /> Projects-->
<!--      <CBadge color="primary" class="mfs-auto">{{ itemsCount }}</CBadge>-->
<!--    </CDropdownItem>-->
<!--    <CDropdownDivider/>-->
<!--    <CDropdownItem>-->
<!--      <CIcon name="cil-shield-alt" /> Lock Account-->
<!--    </CDropdownItem>-->
    <div @click="logout()">
      <CDropdownItem>
        <CIcon name="cil-lock-locked" />Logout
      </CDropdownItem>
    </div>
  </CDropdown>
</template>

<script>
export default {
  name: 'TheHeaderDropdownAccnt',
  methods: {
    logout () {
      this.$session.logout()
      this.$router.push('/login').catch(()=>{});
      location.reload(true)
    }
  },
  data () {
    return { 
      itemsCount: 42
    }
  }
}
</script>

<style scoped>
  .c-icon {
    margin-right: 0.3rem;
  }
.logout-size{
  font-weight: bold;
  width: 100px;
  margin-top: 1px;
}
</style>