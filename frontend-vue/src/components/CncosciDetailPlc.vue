<template>
  <div>
    <v-card :loading="loading" :disabled="loading">
      <v-card-text>
      <abl-document class="abl-page"  :key="cncosci_data_objs.id" ref="report">
        <div class="abl-doc-title">
          <div class="title-text">KAIST IoT 데이터 상세정보(공작기계 진동)</div>
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
              <th colspan="6">TimeStamp</th>
              <th colspan="6">진동 값</th>
            </tr>
            <tr v-for="(item,index) in cncosci_data_objs" :key="index">
              <td colspan="6"><span></span>{{parse_data(item).msg.split(',')[0]}}</td>
              <td colspan="6"><span></span>{{parse_data(item).msg.split(',')[1]}}</td>
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
    cncosci_data: { type: Object, required: true }
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
    async get_cncosci_data(id){
      let params = {
        sensordata_id:id
      };
      let { data } = await this.$http.post("sensordata_all", params);
      this.cncosci_data_objs = data.objects
    },
    parse_data(item){
      var data = JSON.parse(item.data_msg)
      console.log("data :",data)
      return data
    }
  },
  mounted () {
    if(this.cncosci_data != null ){
      this.get_cncosci_data(this.cncosci_data.id)
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
      cncosci_data_objs:null
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