<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> 사용자 리스트 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CCol sm="8">
              <v-text-field outlined dense hide-details
                            placeholder="사용자 정보를 입력하세요"
                            append-icon="mdi-magnify"
                            v-model="filter.querystring"
                            @keydown.enter="query()"
                            class="m-right bg-white"
              />
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="query">
                <v-icon small>mdi-magnify</v-icon>
                <div class="ml-1">검색</div>
              </v-btn>
            </CCol>
            <CCol sm="1">
              <v-btn depressed dark big
                     color="light-blue darken-2"
                     @click="onUserAdd()">
                <v-icon small>mdi-plus</v-icon>
                <div class="ml-1">사용자 추가</div>
              </v-btn>
            </CCol>
          </CNavbar>
        </CCardBody>
      </v-app>
    </CCard>
    <CCard>
      <v-app class="sr-card-app">
        <v-data-table
            height="calc(100vh-100vh)"
            :headers="table.headers"
            :items="table.data"
            :server-items-length="table.total"
            :loading="table.loading"
            :options.sync="table.options"
            :footer-props="{ 'items-per-page-options': [15, 30, 60] }"
            class="elevation-1"
        >
          <template v-slot:item="row">
            <tr>
              <td>{{ row.item._index }}</td>
              <td >{{ row.item.user_id }}</td>
              <td >{{ row.item.user_name }}</td>
              <td >{{ row.item.email }}</td>
              <td> <v-btn outlined x-small rounded color="primary" @click="onUserModify(row.item)">수정</v-btn></td>
              <td> <v-btn outlined x-small rounded color="primary" @click="onUserDelete(row.item)">삭제</v-btn></td>
            </tr>
          </template>
        </v-data-table>
        <v-dialog v-model="usersDialog.show" persistent  max-width="600px" >
          <v-card>
            <div class="sensor-detail-container">
              <v-btn fab x-small dark depressed color="grey darken-1" class="sensor-detail-close" @click="usersDialog.show = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
            </div>
            <CContainer fluid>
              <CRow class="justify-content-center">
                <CCol md="12">
                  <CCard class="mx-4 mb-0">
                    <CCardBody class="p-4">
                      <CForm>
                        <span class="title-msg">{{usersDialog.type_msg}}</span>
                        <CInput
                            placeholder="사용자 아이디"
                            autocomplete="username"
                            v-model="usersDialog.user_id"
                        >
                          <template #prepend-content><CIcon name="cil-user"/></template>
                        </CInput>

                        <CInput
                            placeholder="사용자 이름"
                            autocomplete="username"
                            v-model="usersDialog.user_name"
                        >
                          <template #prepend-content><CIcon name="cil-user"/></template>
                        </CInput>
                        <CInput
                            placeholder="이메일"
                            autocomplete="email"
                            prepend="@"
                            v-model="usersDialog.email"
                        />
                        <CInput
                            placeholder="패스워드"
                            type="password"
                            autocomplete="new-password"
                            v-model="usersDialog.user_pw"
                        >
                          <template #prepend-content><CIcon name="cil-lock-locked"/></template>
                        </CInput>
                        <CInput
                            placeholder="패스워드 확인"
                            type="password"
                            autocomplete="new-password"
                            class="mb-4"
                            v-model="usersDialog.user_pw_valid"
                        >
                          <template #prepend-content><CIcon name="cil-lock-locked"/></template>
                        </CInput>
                        <CButton color="success" block @click="onUserCreate()">{{usersDialog.type_msg}}</CButton>
                      </CForm>
                    </CCardBody>
                  </CCard>
                </CCol>
              </CRow>
            </CContainer>
          </v-card>
        </v-dialog>
        <v-dialog v-model="dialog.show" max-width="500px">
          <v-card>
            <v-card-title>선택한 사용자를 삭제하시겠습니까?</v-card-title>
            <v-card-actions>
              <v-btn tile depressed class="flex-grow-1" @click="deleteUser(dialog.del_item)">삭제</v-btn>
              <v-btn tile depressed class="flex-grow-1" @click="dialog.show = false">취소</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

      </v-app>
    </CCard>

  </div>
</template>

<script>

import axios from 'axios'
import moment from 'moment'
import _ from 'lodash'

export default {
  components: {moment},
  methods: {
    async query() {
      this.table.loading = true;
      const { page, itemsPerPage } = this.table.options;
      let filters_and = []
      let filters_or = []
      filters_and.push({name: 'user_type', op: 'eq', val: 2})
      let q = {
        filters: [{or:filters_or},{and:filters_and}],
        // order_by: [{field: 'apply_date', direction: 'desc'}]
        order_by: [{field: 'user_name', direction: 'asc'}]
      };

      let params = {
        q: JSON.stringify(q),
        page: page,
        results_per_page: itemsPerPage,
      };
      let { data } = await this.$http.get("users", { params });
      this.table.total = data.num_results;
      this.table.loading = false;

      this.table.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (page - 1) * itemsPerPage;
        return v;
      });
    },
    onUserAdd(){
      this.usersDialog.type_msg = '사용자 생성'
      this.usersDialog.user_id=''
      this.usersDialog.user_name=''
      this.usersDialog.user_pw=''
      this.usersDialog.user_pw_valid=''
      this.usersDialog.email=''
      this.usersDialog.show = true
    },
    onUserModify(item){
      this.usersDialog.type_msg = '사용자 수정'
      this.usersDialog.user_id=item.user_id
      this.usersDialog.user_name=item.user_name
      this.usersDialog.user_pw='admin12!@'
      this.usersDialog.user_pw_valid='admin12!@'
      this.usersDialog.email=item.email
      this.usersDialog.show = true
    },
    onUserDelete(item){
      this.dialog.show = true
      this.dialog.del_item = item
    },
    async onUserCreate(){
      let params = {}
      if(this.usersDialog.user_id.length < 4){
        this.err_msg = '사용자 아이디를 확인해 주세요!'
        this.$session.$emit('modal-alert', this.err_msg)
        return
      }
      if(this.usersDialog.user_name.length < 2){
        this.err_msg = '사용자 이름을 확인해 주세요!'
        this.$session.$emit('modal-alert', this.err_msg)
        return
      }
      if(this.usersDialog.email.length < 2){
        this.err_msg = '이메일을 확인해 주세요!'
        this.$session.$emit('modal-alert', this.err_msg)
        return
      }
      if(this.usersDialog.user_pw != 'admin12!@') {
        if (this.usersDialog.user_pw.length < 2) {
          this.err_msg = '비밀번호를 확인해 주세요!'
          this.$session.$emit('modal-alert', this.err_msg)
          return
        } else {
          if (this.usersDialog.user_pw.length > 0) {
            if (this.usersDialog.user_pw.length < 8) {
              this.err_msg = '비밀번호를 확인해주세요!(8자리 이상)'
              this.$session.$emit('modal-alert', this.err_msg)
              return
            }
            if (!/^[a-zA-Z0-9~!@#$%^&*()_+|<>?:{}]+$/.test(this.usersDialog.user_pw)) {
              this.err_msg = '비밀번호를 확인해주세요!(특수문자 포함)'
              this.$session.$emit('modal-alert', this.err_msg)
              return
            }
            if (this.usersDialog.user_pw !== this.usersDialog.user_pw_valid) {
              this.err_msg = '비밀번호를 확인해주세요!'
              this.$session.$emit('modal-alert', this.err_msg)
              return
            }
          }
        }
      }
      params.user_id = this.usersDialog.user_id;
      params.user_name = this.usersDialog.user_name;
      params.user_pw = this.usersDialog.user_pw;
      params.email = this.usersDialog.email;
      params.user_type=2
      if(this.usersDialog.type_msg == '사용자 생성') {
        let {data} = await this.$http.post(`user_register`, params)
        if (data.register_result == 1) {
          this.$session.$emit('modal-alert', '사용자등록처리가 정상처리 되었습니다.')
          this.usersDialog.show = false
          this.query();
        } else if (data.register_result == 0) {
          this.$session.$emit('modal-alert', '이미 등록되어 있는 사용자 입니다.')
        }
      }else{
        let {data} = await this.$http.post(`user_modify`, params)
        if (data.register_result == 1) {
          this.$session.$emit('modal-alert', '사용자 수정처리가 정상처리 되었습니다.')
          this.usersDialog.show = false
          this.query();
        }
      }

    },
    async deleteUser(item){
      this.dialog.show = false
      await this.$http.delete(`users/${item.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다')
      this.query();
    }
  },
  mounted() {
    if(!this.$session.authorized){
      location.reload(true)
      return
    }
  },
  computed: {
  },
  watch: {
    "table.options": {
      handler() {
        this.query();
      },
      deep: true,
    },
  },
  data() {
    return {
      filter: {
        querystring: "",
      },
      table: {
        headers: [
          { text: "No.", value: "id", sortable: false, width: 40 },
          { text: "사용자 아이디", value: "user_id", sortable: false,align: "center", width: 100 },
          { text: "사용자 이름", value: "user_name", sortable: false,align: "center", width: 100 },
          { text: "사용자 이메일", value: "email", sortable: false,align: "center", width: 100 },
          {text: "수정", value: "",  sortable: false, align: "center", width: 100 },
          {text: "삭제", value: "", sortable: false, align: "center", width: 100 },
        ],
        loading: false,
        total: 0,
        options: {},
        data: [],
      },
      selected_option:null,
      options_array : [
      ],
      usersDialog: {
        show: false,
        data: null,
        user_id:'akj2995',
        user_name:'안근진',
        user_pw:'akj2995!@',
        user_pw_valid:'akj2995!@',
        email:'akj2995@daum.net',
        type_msg:'사용자 생성'
      },
      dialog:{
        show:false,
        del_item:null,
      },
      err_msg:''
    };
  },
};
</script>
<style scoped lang="scss">
.sr-card-app{
  height:350px;
}
.sr-card-app-title{
  height:160px;
}
.sensor-detail-container {
  position: relative;
}
.sensor-detail-container-2 {
  position: relative;
  width: 1200px;
  height:500px
}

.sensor-detail-close {
  position: absolute;
  top: 20px; right: 10px;
  z-index: 10;
}
.m-right{margin-right: 20px;}
.text-center{
  text-align: center;
}
td {
  text-align: center;
}
.m-left{margin-left: 10px;}

.title-msg{

  font-size: 20px;
  font-weight: bold;
  text-align: center;
  margin-bottom: 5px;
}
</style>