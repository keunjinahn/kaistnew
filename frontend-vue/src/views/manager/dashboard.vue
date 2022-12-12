<template>
    <div>
        <v-app>
          <CCard>
            <CCardBody>
                <CCol sm="2">
                    <v-select outlined dense hide-details
                              v-model="selected_range_value"
                              :items="range_list"
                              label="조회구간"
                              item-text="name"
                              item-value="value"
                              @change="onChangeRange()"
                              class="bg-white"
                    />
                </CCol>
            </CCardBody>
          </CCard>
          <CCard>
            <div class="sensor-detail-container-2">
                <highcharts
                        constructor-type="chart"
                        :options="chart6Option_osci_1"
                        class="hi-weight"
                />
            </div>
            <div class="sensor-detail-container-2">
                <highcharts
                        constructor-type="chart"
                        :options="chart6Option_osci_2"
                        class="hi-weight"
                />
            </div>
          </CCard>
        </v-app>
        <!--    <div class="sensor-detail-container-2">-->
        <!--      <highcharts-->
        <!--              constructor-type="chart"-->
        <!--              :options="chart6Option"-->
        <!--              class="hi-weight"-->
        <!--      />-->
        <!--    </div>-->
    </div>
</template>

<script>
import axios from 'axios'
import moment from 'moment'
import _ from 'lodash'

const chartOptions = {
    // chart: { zoomType: 'xy' },
    title: {text: null},
    colors: ['skyblue', 'orange'],
    xAxis: [{categories: [], crosshair: false}],
    yAxis: [
        {
            labels: {format: '{value:,f}'},
            title: {text: '진동 값'}
        }
    ],
    credits: {enabled: false},
    tooltip: {shared: true, crosshair: false},
    series:[
      { data: [],type: 'line', name: 'value', lineWidth: 1},
    ],
}

export default {
    components: {moment},
    methods: {
      async query1() {
        if(this.refresh_cnt > 60){
          location.reload(true)
          return
        }
        let params = {
          range_value:this.selected_range_value
        }

        let { data } = await this.$http.post("sensor_data_range", params)
        .catch(error => {
          console.log(error.response.data.message || error.message)
          this.refresh_cnt += 1
          if(this.$route.path == '/manager/dashboard')
            this.startInterval()
        });
        console.log(JSON.stringify(data))
        this.cncosci_data_objs.cate_1 = []
        this.cncosci_data_objs.osci_1 = []
        this.cncosci_data_objs.cate_2 = []
        this.cncosci_data_objs.osci_2 = []
        if(data.sensor_list_1.length > 0) {
          this.cncosci_data_objs.cate_1 = data.sensor_list_1.map(v => v.created_date.slice(-8))
          this.cncosci_data_objs.osci_1 = data.sensor_list_1.map((v, index) => ({
            x: v.index,
            y: Number(JSON.parse(v.data_msg).msg.split(',')[1])
          }))
        }
        if(data.sensor_list_1.length > 0) {
          this.cncosci_data_objs.cate_2 = data.sensor_list_2.map(v => v.created_date.slice(-8))
          this.cncosci_data_objs.osci_2 = data.sensor_list_2.map((v, index) => ({
            x: v.index,
            y: Number(JSON.parse(v.data_msg).msg.split(',')[1])
          }))
        }
        // this.cncosci_data_objs.cate_1 = data.sensor_list_1.map(v => v.created_date.slice(-8))
        // alert(JSON.stringify(this.cncosci_data_objs.cate_1))
        console.log("data=> cnt : " + this.refresh_cnt + ",$route.path : " + this.$route.path)
        this.refresh_cnt += 1
        if(this.$route.path == '/manager/dashboard')
          this.startInterval()
      },
      onChangeRange(){
          this.query1()
      },
      startInterval () {
        clearTimeout(this.sensors.tick)
        this.sensors.tick = setTimeout(async () => {
          this.query1();
        }, 2000)
      },
    },
    mounted() {
        if (!this.$session.authorized) {
            location.reload(true)
            return
        }
        this.selected_range_value = this.range_list[3].value
        this.query1();
        // this.refresh_home()
    },
    computed: {
        chart6Option_osci_1() {
            let obj = _.cloneDeep(chartOptions)
            obj.series[0].data = this.cncosci_data_objs.osci_1.map(v => v.y)
            obj.xAxis[0].categories = this.cncosci_data_objs.cate_1
            obj.yAxis[0].title.text = 'CNC 1번 진동'
            return obj
        },
        chart6Option_osci_2() {
          let obj = _.cloneDeep(chartOptions)
          obj.series[0].data = this.cncosci_data_objs.osci_2.map(v => v.y)
          obj.xAxis[0].categories = this.cncosci_data_objs.cate_2
          obj.yAxis[0].title.text = 'CNC 2번 진동'
          return obj
        },

        // refresh_home () {
        //   clearTimeout(this.sensors.tick)
        //   this.sensors.tick = setTimeout(async () => {
        //     location.reload(true)
        //   }, 10 * 1000)
        // },
    },
    data() {
        return {
            sensorDetail: {
                show: false,
                data: null,
            },
            sensorGraph: {
                show: true,
                data: null,
            },
            sensors: {
                loaded: false,
                tick: null,
            },
            download_file_index: 0,
            cncosci_data_objs: {
              osci_1: [],
              osci_2: [],
              cate_1: [],
              cate_2: [],
            },
            selected_range :null,
            selected_range_value:0,
            range_list : [
              {name:'일',value:1},
              {name:'시간',value:2},
              {name:'10분',value:3},
              {name:'분',value:4},
            ],
            refresh_cnt:0
        };
    },
};
</script>
<style scoped lang="scss">
    .sr-card-app {
        height: 350px;
    }

    .sr-card-app-title {
        height: 160px;
    }

    .sensor-detail-container {
        position: relative;
    }

    .sensor-detail-container-2 {
        position: relative;
        width: 100%;
        height: 400px
    }

    .sensor-detail-close {
        position: absolute;
        top: 20px;
        right: 10px;
        z-index: 10;
    }

    .m-right {
        margin-right: 20px;
    }

    .text-center {
        text-align: center;
    }

    td {
        text-align: center;
    }

    .m-left {
        margin-left: 10px;
    }

    .hi-weight {
        height: 400px;
    }
</style>