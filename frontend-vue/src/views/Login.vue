<template>
  <div class="c-app flex-row align-items-center login-main">
    <CContainer>
      <CRow class="justify-content-center">
        <CCol md="8">
          <CCardGroup>
            <CCard class="p-4">
              <CCardBody>
                <CForm>
                  <h1>KAIST IoT 데이터 <br>관리 시스템</h1>
                  <p class="text-muted"></p>
                  <CInput
                    placeholder="사용자 아이디"
                    autocomplete="username email"
                    v-model="form.username"
                  >
                    <template #prepend-content><CIcon name="cil-user"/></template>
                  </CInput>
                  <CInput
                    placeholder="패스워드"
                    type="password"
                    autocomplete="curent-password"
                    v-model="form.password"
                    @keypress.enter="requestGetToken"
                  >
                    <template #prepend-content><CIcon name="cil-lock-locked"/></template>
                  </CInput>
                  <CRow>
                    <CCol col="6" class="text-left">
                      <CButton color="secondary" class="px-4" @click="requestGetToken" >로그인</CButton>
                    </CCol>
                  </CRow>
                </CForm>
              </CCardBody>
            </CCard>
            <CCard
              color="primary"
              text-color="white"
              class="text-center py-5 d-md-down-none"
              body-wrapper
            >
              <CCardBody>
                <h2>공지사항</h2>
                <span>카이스트 IoT 데이터 관리 시스템 오픈</span>
              </CCardBody>
            </CCard>
          </CCardGroup>
        </CCol>
      </CRow>
    </CContainer>
  </div>
</template>

<script>
export default {
  name: 'Login',
  methods: {
    async requestGetToken () {
      this.error = null
      if (!this.form.username || !this.form.password)
        return (this.error = '아이디와 패스워드를 입력해 주세요.')

      this.loading = true
      try {
        let {data} = await this.$http.post('login', this.form)
        // if(this.form.password != 'kitech!@'){
        //   alert("패스워드 오류!!")
        //   location.reload(true)
        //   return data
        // }

        if (data.status) {
          await this.$session.setToken(data.user)
          this.$router.push('/manager/injectiondata')
        }else {
          if (data.reason == 1) {
            alert('로그인이 실패(아이디를 확인하여주세요!)')
          } else if (data.reason == 2) {
            alert('로그인이 실패(패스워드를 확인하여주세요!)')
          }
        }
        return data
      }
      catch (err) {
        this.error = err.message
      }
      finally {
        this.loading = false
      }

    },
    move_first(){
      location.reload(true)
    },
    beforeDestroy () {
      // document.removeEventListener("backbutton", this.move_first());
    }
  },
  mounted() {
    window.onpopstate = function() {
      location.reload(true)
    };
  },
  data () {
    return {
      loading: false,
      form: {
        username: '',
        password: ''
      },
      error: null,
    }
  }
}
</script>
<style lang="scss" scoped>
.login-main {
  background-color: #E6EEFF !important;
  background-image: url('~@/assets/bg/bg-2.jpg');
  background-size: cover;
  background-position: center center;
}
</style>
