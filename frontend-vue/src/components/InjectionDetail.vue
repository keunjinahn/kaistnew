<template>
  <div>
    <v-card :loading="loading" :disabled="loading">
      <v-card-text>
      <abl-document class="abl-page"  :key="injection_data.id" ref="report">
        <div class="abl-doc-title">
          <div class="title-text">KAIST IoT 사출기 데이터 상세정보(INJECTION)</div>
        </div>
        <div class="abl-doc-body">
          <br>
          <table class="abl-table-ts">
            <colgroup>
            </colgroup>
            <tr>
              <th colspan="1">CycleCount</th>
              <th colspan="1">TempZone1</th>
              <th colspan="1">TempZone2</th>
              <th colspan="1">TempZone3</th>
              <th colspan="1">TempZone4</th>
              <th colspan="1">TempZone5</th>
              <th colspan="1">CycleTime</th>
              <th colspan="1">InjectTime</th>
              <th colspan="1">Cushion(mm)</th>
              <th colspan="1">Cushion(cm3)</th>
              <th colspan="1">InjectPress</th>
              <th colspan="1">Alarms</th>
            </tr>
            <tr v-for="(item,index) in injection_data_objs" :key="index">
              <td colspan="1"><span></span>{{parse_data(item,0)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,1)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,2)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,3)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,4)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,5)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,6)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,7)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,8)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,9)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,10)}}</td>
              <td colspan="1"><span></span>{{parse_data(item,11)}}</td>
            </tr>
          </table>
          <br>
        </div>
      </abl-document>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import AblDocument from '@/components/AblDocument'
import AblTextarea from '@/components/AblTextarea'
import axios from 'axios'
import moment from 'moment'
export default {
  props: {
    injection_data: { type: Object, required: true }
  },
  components: {AblDocument, AblTextarea},
  methods: {
    async attach_download(attach_filename) {
      var url = '/api/monitor/v1/upload_file/' + attach_filename
      axios({
        method: 'get',
        url: url,
        // url: 'search_result.xlsx',
        responseType: 'blob'
      })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data], {
              type: 'application/vnd.ms-excel'
            }))
            const link = document.createElement('a')
            link.href = url
            link.setAttribute('download', attach_filename) // or any other extension
            document.body.appendChild(link)
            link.click()
          })
          .catch(() => console.log('error occured'))
    },
    async get_injection_data(id){
      let filters_and = []
      let filters_or = []
      filters_and.push({name: 'fk_sensor_file_id', op: 'eq', val: id})
      let q = {
        filters: [{or:filters_or},{and:filters_and}],
        order_by: [{field: 'id', direction: 'asc'}]
      };

      let params = {
        q: JSON.stringify(q),
      };
      let { data } = await this.$http.get("sensordata", { params });
      this.injection_data_objs = data.objects
    },
    parse_data(item,index){
      console.log("item :",JSON.stringify(item))
      var data1 = JSON.parse(item.data_msg)
      console.log("data1 :",data1)
      var data_msg = JSON.parse(item.data_msg).msg.split(',')[index]
      return data_msg
    }
  },
  mounted () {
    if(this.injection_data != null ){
      this.get_injection_data(this.injection_data.id)
    }
  },
  data () {
    return {
      preview: null,
      loading: false, 
      school: {},
      refresh_id:0,
      s3_data_json:null,
      deleteDialog:{
        show: false,
        delItem:''
      },
      market_file_input:null,
      file_path:null,
      file_name: '파일을 선택해 주세요',
      pdf_file_input:null,
      pdf_file_path:null,
      pdf_file_name: '파일을 선택해 주세요',
      thumb_file_input:null,
      thumb_file_path:null,
      thumb_file_name: '파일을 선택해 주세요',
      selected_tech_type:null,
      previews:[],
      pdf_save_flag:false,
      pdfDialog:{
        show:false
      },
      injection_data_objs:null
    }
  }
}
</script>

<style lang="scss" scoped>
.t1 {
  text-align: justify;
  text-align-last: justify;
  flex: 1 0 auto;
  padding: 0 10px;
}
.abl-page {
  padding: 15px 30px;
}
.school-file-upload {
  position: relative;
  top: 0px; left: 10px;
  z-index: 10;
}
.school-save {
  position: relative;
  top: -10px; left:15px;
  z-index: 10;
}
.report-download {
  position: relative;
  top: -10px; left:780px;
  z-index: 10;
}
.image-left-m{
  overflow: hidden;
  text-align: center;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
.td-bold{
  background-color: #e7e7e7;
}
.image-default-h{
  height:26px !important;
  text-align: center;
}
.f-pos{
  position: fixed;
  top: -1000px; left: 0;
}
.abl-doc-body{
  width: 740px;
}
.abl-page{
  width: 800px;
}
th {
  text-align: center;
}
.s-size{
  margin: 5px 5px;
  font-size: 12px;
}
.f-size {
  font-size: 12px;
}
.m-top{
  margin-top: 20px;
}
.ta-align{
  text-align: left;
  font-size: 12px;
}
.ta-align-center{
  text-align: center;
}

</style>