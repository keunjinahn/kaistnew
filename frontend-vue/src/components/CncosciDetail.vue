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
              <th colspan="1">FFT or 1/3 Octave</th>
              <th colspan="1">FFT Unit</th>
              <th colspan="1">SamplingPeriod us</th>
              <th colspan="1">SamplingCount</th>
            </tr>
            <tr >
              <td colspan="1"><span></span>{{cncosci_data_objs[0].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[1].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[2].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[3].split(',')[1]}}</td>
            </tr>
            <tr>
              <th colspan="1">FrequencyResolution Hz</th>
              <th colspan="1">Window type</th>
              <th colspan="1">OverlapRatio %</th>
              <th colspan="1">TotalSamplingTime s</th>
            </tr>
            <tr >
              <td colspan="1"><span></span>{{cncosci_data_objs[4].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[5].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[6].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[7].split(',')[1]}}</td>
            </tr>
            <tr>
              <th colspan="1">FFTCountPer1Trigger</th>
              <th colspan="1">AverageProcess</th>
              <th colspan="1">SamplingDelayTimer 1ms</th>
              <th colspan="1">CurrentFFTCount</th>
            </tr>
            <tr >
              <td colspan="1"><span></span>{{cncosci_data_objs[8].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[9].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[10].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[11].split(',')[1]}}</td>
            </tr>
          </table>
          <table class="abl-table-ts">
            <colgroup>
            </colgroup>
            <tr>
              <th colspan="12">FrequencyRange Hz</th>
            </tr>
            <tr>
              <th colspan="1">Block1</th>
              <th colspan="1">Block2</th>
              <th colspan="1">Block3</th>
              <th colspan="1">Block4</th>
              <th colspan="1">Block5</th>
              <th colspan="1">Block6</th>
              <th colspan="1">Block7</th>
              <th colspan="1">Block8</th>
              <th colspan="1">Block9</th>
              <th colspan="1">Block10</th>
            </tr>
            <tr >
              <td colspan="1"><span></span>{{cncosci_data_objs[14].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[15].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[16].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[17].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[18].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[19].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[20].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[21].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[22].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[23].split(',')[1]}}</td>

             </tr>
          </table>
          <table class="abl-table-ts">
            <colgroup>
            </colgroup>
            <tr>
              <th colspan="5">{{cncosci_data_objs[24].split(',')[1]}}</th>
            </tr>
            <tr>
              <th colspan="1">RMS</th>
              <th colspan="1">TimeAxisPeak</th>
              <th colspan="1">CF</th>
              <th colspan="1">OA</th>
              <th colspan="1">Peak</th>
            </tr>
            <tr >
              <td colspan="1"><span></span>{{cncosci_data_objs[25].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[26].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[27].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[28].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[29].split(',')[1]}}</td>
            </tr>
          </table>
          <table class="abl-table-ts">
            <colgroup>
            </colgroup>
            <tr>
              <th colspan="1">POA1</th>
              <th colspan="1">POA2</th>
              <th colspan="1">POA3</th>
              <th colspan="1">POA4</th>
              <th colspan="1">POA5</th>
              <th colspan="1">POA6</th>
              <th colspan="1">POA7</th>
              <th colspan="1">POA8</th>
              <th colspan="1">POA9</th>
              <th colspan="1">POA10</th>
            </tr>
            <tr >
              <td colspan="1"><span></span>{{cncosci_data_objs[30].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[32].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[34].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[36].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[38].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[40].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[42].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[44].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[46].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[48].split(',')[1]}}</td>

            </tr>
            <tr>
              <th colspan="1">Peak1</th>
              <th colspan="1">Peak2</th>
              <th colspan="1">Peak3</th>
              <th colspan="1">Peak4</th>
              <th colspan="1">Peak5</th>
              <th colspan="1">Peak6</th>
              <th colspan="1">Peak7</th>
              <th colspan="1">Peak8</th>
              <th colspan="1">Peak9</th>
              <th colspan="1">Peak10</th>
            </tr>
            <tr >
              <td colspan="1"><span></span>{{cncosci_data_objs[31].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[33].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[35].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[37].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[39].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[41].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[43].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[45].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[47].split(',')[1]}}</td>
              <td colspan="1"><span></span>{{cncosci_data_objs[49].split(',')[1]}}</td>

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
      alert(JSON.stringify(data))
      this.cncosci_data_objs = data.objects[0]
      var msg = JSON.parse(this.cncosci_data_objs.data_msg)
      this.cncosci_data_objs = msg.msg
      // this.cncosci_data_objs= JSON.parse(this.cncosci_data_objs.data_msg)
      // alert(this.cncosci_data_objs)
    },
    parse_data(){
      console.log("item 1:",JSON.stringify(this.cncosci_data_objs))
      var data1 = JSON.parse(this.cncosci_data_objs.data_msg)
      console.log("data1 :",data1)
      return ''
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