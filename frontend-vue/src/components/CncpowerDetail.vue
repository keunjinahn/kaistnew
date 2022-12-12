<template>
  <div>
    <v-card :loading="loading" :disabled="loading">
      <v-card-text>
      <abl-document class="abl-page"  :key="cncpower_data_objs.id" ref="report">
        <div class="abl-doc-title">
          <div class="title-text">KAIST IoT 데이터 상세정보(공작기계 전력)</div>
        </div>
        <div class="abl-doc-body">
          <br>
          <table class="abl-table-ts">
            <colgroup>
            </colgroup>
            <tr>
              <th colspan="12">진동 센서 데이터</th>
            </tr>
            <tr>
              <th colspan="5">TimeStamp</th>
              <th colspan="1">전력 센서1 전류량</th>
              <th colspan="1">전력 센서2 전류량</th>
              <th colspan="1">전력 센서3 전류량</th>
              <th colspan="1">전력 센서1 전력량</th>
              <th colspan="1">전력 센서2 전력량</th>
              <th colspan="1">전력 센서3 전력량</th>
              <th colspan="1">총 전력량</th>
            </tr>
            <tr v-for="(item,index) in cncpower_data_objs" :key="index">
              <td colspan="5"><span></span>{{parse_data(item).split(',')[0]}}</td>
              <td colspan="1"><span></span>{{parse_data(item).split(',')[1]}}</td>
              <td colspan="1"><span></span>{{parse_data(item).split(',')[2]}}</td>
              <td colspan="1"><span></span>{{parse_data(item).split(',')[3]}}</td>
              <td colspan="1"><span></span>{{parse_data(item).split(',')[4]}}</td>
              <td colspan="1"><span></span>{{parse_data(item).split(',')[5]}}</td>
              <td colspan="1"><span></span>{{parse_data(item).split(',')[6]}}</td>
              <td colspan="1"><span></span>{{parse_data(item).split(',')[7]}}</td>
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
    cncpower_data: { type: Object, required: true }
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
    async get_cncpower_data(id){
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
      this.cncpower_data_objs = data.objects

    },
    parse_data(item){
      var data1 = JSON.parse(item.data_msg.replace('\n','')).msg
      return data1
      //return ''
    }
  },
  mounted () {
    if(this.cncpower_data != null ){
      this.get_cncpower_data(this.cncpower_data.id)
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
      cncpower_data_objs:null
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
  width: 1100px;
}
.abl-page{
  width: 1200px;
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