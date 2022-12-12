<template>
  <div>
    <CCard>
      <v-app class="sr-card-app-title">
        <CCardHeader>
          <CIcon name="cil-justify-center"/>
          <strong> KAIST 공작기계 전력 데이터 </strong>
        </CCardHeader>
        <CCardBody>
          <CNavbar
              expandable="md"
              color="light"
          >
            <CCol sm="2">
              <v-select outlined dense hide-details
                        v-model="selected_ch"
                        :items="channel_list"
                        label="채널"
                        item-text="text"
                        item-value="value"
                        @change="onChangeChannel()"
                        class="bg-white"
              />
            </CCol>
            <!--            <CCol sm="2">-->
            <!--              <v-text-field outlined dense hide-details readonly-->
            <!--                            label="시작일"-->
            <!--                            v-model="search.dialog.form.start_date"-->
            <!--                            @click="setSearchDatetime(search.dialog.form,'start_date')"-->
            <!--              />-->
            <!--            </CCol>-->
            <!--            ~-->
            <!--            <CCol sm="2">-->
            <!--              <v-text-field outlined dense hide-details readonly-->
            <!--                            label="종료일"-->
            <!--                            v-model="search.dialog.form.end_date"-->
            <!--                            @click="setSearchDatetime(search.dialog.form,'end_date')"-->
            <!--              />-->
            <!--            </CCol>-->
            <CCol sm="8">
              <v-text-field outlined dense hide-details
                            placeholder="파일 이름을 입력하세요"
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
              <td class="clickable-row" >{{ row.item.file_names }}</td>
              <td class="clickable-row" >{{ row.item.sensor_num }}</td>
              <td> {{row.item.created_date | moment('YYYY-MM-DD HH:mm:ss')}}</td>
              <td> <v-btn outlined x-small rounded color="primary" @click="onSensorDetailHandler(row.item)">상세보기</v-btn></td>              
              <td> <v-btn outlined x-small rounded color="primary" @click="onSensorGraphHandler(row.item)">그래프</v-btn></td>
              <td> <v-btn outlined x-small rounded color="primary" @click="csv_download(row.item)">다운로드</v-btn></td>
            </tr>
          </template>
        </v-data-table>
        <v-dialog v-model="sensorDetail.show" persistent max-width="1200px" >
          <v-card>
            <div class="sensor-detail-container">
              <v-btn fab x-small dark depressed color="grey darken-1" class="sensor-detail-close" @click="sensorDetail.show = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <cncpower-detail @callBackEvent="onEmitEvent" :cncpower_data="sensorDetail.data" />
            </div>
          </v-card>
        </v-dialog>
        <v-dialog v-model="sensorGraph.show" persistent max-width="1200px">
          <v-card >
            <div class="sensor-detail-container-2">
              <CCardHeader>
                <CIcon name="cil-justify-center"/>
                <strong> KAIST IoT 데이터 그래프(공작기계 전력) </strong>
              </CCardHeader>
              <v-btn fab x-small dark depressed color="grey darken-1" class="sensor-detail-close" @click="sensorGraph.show = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>
              <highcharts
                  constructor-type="chart"
                  :options="chart6Option"
              />
            </div>
          </v-card>
        </v-dialog>
        <v-dialog v-model="search.datetime.show" width="300" overlay-opacity="0.9">
          <div class="white">
            <div class="d-flex white">
              <v-date-picker no-title v-model="search.datetime.date" />
            </div>
            <div class="d-flex pa-2">
              <v-btn class="flex-grow-1" tile depressed @click="search.datetime.show=false">취소</v-btn>
              <v-btn
                  class="flex-grow-1 ml-2"
                  tile
                  depressed
                  color="primary"
                  @click="saveSearchDatetime">
                선택
              </v-btn>
            </div>
          </div>
        </v-dialog>
      </v-app>
    </CCard>

  </div>
</template>

<script>
import CncpowerDetail from '@/components/CncpowerDetail'
import axios from 'axios'
import moment from 'moment'
import _ from 'lodash'

const chartOptions = {
  // chart: { zoomType: 'x' },
  title: { text: null },
  colors: ['skyblue', 'orange'],
  xAxis: [{ categories: [], crosshair: false }],
  yAxis: [
    {
      labels: {format: '{value:,f}'},
      title: {text: 'Watt'}
    }
  ],
  credits: {enabled: false},
  tooltip: {shared: true, crosshair: false},
  series: [
      { data: [],type: 'line', name: '전력 센서1 전류량', lineWidth: 1},
      { data: [],type: 'line', name: '전력 센서2 전류량', lineWidth: 1 },
      { data: [],type: 'line', name: '전력 센서3 전류량', lineWidth: 1 },
      { data: [],type: 'line', name: '전력 센서1 전력량', lineWidth: 1 },
      { data: [],type: 'line', name: '전력 센서2 전력량', lineWidth: 1 },
      { data: [],type: 'line', name: '전력 센서3 전력량', lineWidth: 1 },
      { data: [],type: 'line', name: '총 전력량', lineWidth: 1 },
  ]
}
export default {
  components: {CncpowerDetail,moment},
  methods: {
    async query() {
      this.table.loading = true;
      const { page, itemsPerPage } = this.table.options;
      let filters_and = []
      let filters_or = []
      filters_and.push({name: 'sensor_type', op: 'eq', val: 'POWER'})
      if(this.selected_ch != '전체')
        filters_and.push({name: 'sensor_num', op: 'eq', val: this.selected_ch})
      if (this.filter.querystring.length > 0) {
        filters_or.push({name: 'file_names', op: 'like', val: "%"+this.filter.querystring+"%"})
      }

      let q = {
        filters: [{or:filters_or},{and:filters_and}],
        // order_by: [{field: 'apply_date', direction: 'desc'}]
        order_by: [{field: 'id', direction: 'desc'}]
      };

      let params = {
        q: JSON.stringify(q),
        page: page,
        results_per_page: itemsPerPage,
      };
      let { data } = await this.$http.get("sensorfiles", { params });
      this.table.total = data.num_results;
      this.table.loading = false;

      this.table.data = data.objects.map((v, i) => {
        v._index = data.num_results - i - (page - 1) * itemsPerPage;
        return v;
      });
    },

    changeOption(){
      this.selected_option = this.options_array.find(v=>v.option_name == this.selected_option)
      this.query();
    },
    onSensorDetailHandler (sensorData) {
      this.dialog.refresh_id += 1
      this.sensorDetail.data = sensorData
      this.sensorDetail.show = true
    },
    onPatentAddHandler () {
      this.sensorDetail.data = null
      this.sensorDetail.show = true
    },
    check_item(file_name){
      if(file_name != undefined && file_name != '' && file_name.length > 3)
        return true
      return false
    },
    async attach_download(attach_filename) {
      var url = '/api/v1/upload_file/' + attach_filename
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
    onEmitEvent(type){
      if(type == "upload"){
        this.query();
      }else if(type == "add"){
        this.query();
      }
      this.patentDetail.show = false
    },
    async deletePatent(item) {
      this.dialog.del_show = false
      await this.$http.delete(`sources/${item.id}`)
      this.$session.$emit('modal-alert', '삭제되었습니다')
      this.query();
    },
    delPatent(row) {
      this.dialog.del_show = true
      this.dialog.del_item = row.item
    },
    async onFileChangeHandler (evt) {
      if (evt.target && evt.target.files && evt.target.files[0]) {
        this.file_post_upload(evt.target.files[0],true)
      }
      else return null
    },
    async file_post_upload(pdf_file) {
      const fd = new FormData()
      fd.append('file', pdf_file)
      let {data} = await this.$http.post('pdf_upload', fd)
      console.log("data.filename :" + JSON.stringify(data.filename))
      if (!data || !data.result || !data.filename)
        return alert("저장실패!!")

    },
    async csv_download(item) {
      this.download_file_index += 1
      let params = {
        id:item.id,
        file_names:item.file_names,
        sensor_type:item.sensor_type
      }
      let {data} = await this.$http.get("csv_download",{params});
      var url = this.$getWebURL() + '/api/v1/download/' + data.filename
      axios({
        method: 'get',
        url:url,
        responseType: 'blob'
      })
          .then(response => {
            const url = window.URL.createObjectURL(new Blob([response.data], {
              type: 'application/vnd.ms-excel'
            }))
            const link = document.createElement('a')
            link.href = url
            var download_file_name = 'kaist_iot_' + data.filename
            link.setAttribute('download', download_file_name) // or any other extension
            document.body.appendChild(link)
            link.click()
          })
          .catch(() => console.log('error occured'))
    },
    setSearchDatetime(form, datakey) {
      let dt = form[datakey].split(/\s+/);
      this.search.datetime.form = form;
      this.search.datetime.datakey = datakey;
      this.search.datetime.date = dt[0];
      this.search.datetime.show = true;
    },
    saveSearchDatetime() {
      this.search.datetime.form[this.search.datetime.datakey] = this.search.datetime.date;
      this.search.datetime.show = false;
    },
    onSensorGraphHandler (sensorData) {
      this.dialog.refresh_id += 1
      this.sensorGraph.data = sensorData
      this.sensorGraph.show = true
      this.get_cncpower_data(this.sensorGraph.data.id,this.sensorGraph.data.file_names)
    },
    async get_cncpower_data(id,file_names){
      
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
      this.cncpower_data_cate = data.objects.map(v => v.created_date.slice(-8))
      this.cncpower_data_objs = data.objects.map((v,index) => ({
        x: index,
        y_1: Number(JSON.parse(v.data_msg.replace('\n','')).msg.split(',')[1]),
        y_2: Number(JSON.parse(v.data_msg.replace('\n','')).msg.split(',')[2]),
        y_3: Number(JSON.parse(v.data_msg.replace('\n','')).msg.split(',')[3]),
        y_4: Number(JSON.parse(v.data_msg.replace('\n','')).msg.split(',')[4]),
        y_5: Number(JSON.parse(v.data_msg.replace('\n','')).msg.split(',')[5]),
        y_6: Number(JSON.parse(v.data_msg.replace('\n','')).msg.split(',')[6]),
        y_7: Number(JSON.parse(v.data_msg.replace('\n','')).msg.split(',')[7]) * 1000
      }))
    },
    onChangeChannel(){

    },
    async get_channels(){
      let filters_and = []
      let filters_or = []
      filters_and.push({name: 'sensor_type', op: 'eq', val: 'POWER'})
      let q = {
        filters: [{or:filters_or},{and:filters_and}],
        order_by: [{field: 'id', direction: 'asc'}]
      };

      let params = {
        q: JSON.stringify(q),
      };
      let { data } = await this.$http.get("sensorfiles", { params });
      let sensor_nums = data.objects.map(v=>({"sensor_num":v.sensor_num}))
      let group = _.groupBy(sensor_nums,"sensor_num");

      this.channel_list = ["전체"].concat(Object.keys(group))
      this.selected_ch = this.channel_list[0]
    },
  },
  mounted() {
    if(!this.$session.authorized){
      location.reload(true)
      return
    }
    this.get_channels()
  },
  computed: {
    years () {
      const year = new Date().getFullYear()
      return Array.from({length: year - 1989}, (value, index) => year - index)
    },
    chart6Option () {
      let obj = _.cloneDeep(chartOptions)
      if(this.cncpower_data_objs.length > 0) {
        obj.xAxis[0].categories = this.cncpower_data_cate
        obj.series[0].data = this.cncpower_data_objs.map(v => v.y_1)
        obj.series[1].data = this.cncpower_data_objs.map(v => v.y_2)
        obj.series[2].data = this.cncpower_data_objs.map(v => v.y_3)
        obj.series[3].data = this.cncpower_data_objs.map(v => v.y_4)
        obj.series[4].data = this.cncpower_data_objs.map(v => v.y_5)
        obj.series[5].data = this.cncpower_data_objs.map(v => v.y_6)
        obj.series[6].data = this.cncpower_data_objs.map(v => v.y_7)
      }
      return obj
    },
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
          { text: "파일명", value: "file_names", sortable: false,align: "center", width: 100 },
          { text: "채널번호", value: "sensor_num", sortable: false,align: "center", width: 100 },
          { text: "생성일자", value: "created_date", sortable: false,align: "center", width: 100 },
          {text: "상세보기", value: "",  sortable: false, align: "center", width: 100 },          
          {text: "그래프", value: "",  sortable: false, align: "center", width: 100 },
          {text: "다운로드", value: "", sortable: false, align: "center", width: 100 },
        ],

        loading: false,
        total: 0,
        options: {},
        data: [],
      },
      selected_option:null,
      options_array : [
      ],
      sensorDetail: {
        show: false,
        data: null,
      },
      dialog: {
        refresh_id :1,
        show: false,
        form: null,
        del_show:false,
        deleted_show:false,
        del_item:null,
      },
      years_type:[],
      tech_types:[],
      selected_year:null,
      selected_tech:null,
      download_file_index:0,
      sensorGraph: {
        show: false,
        data: null,
      },
      cncpower_data_objs:[],
      cncpower_data_cate : [],
      search: {
        dialog: {
          show: false,
          form: {
            acci_start_date: moment().format("YYYY-MM-DD"),
            acci_end_date: moment().format("YYYY-MM-DD"),
          },
          selected_search_type:null,
          selected_search_type_code:0,
        },
        datetime: {
          show: false,
          date: "",
          time: "",
        },
      },
      selected_ch:"전체",
      channel_list:[]
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
</style>