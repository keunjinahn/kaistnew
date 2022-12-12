import _ from 'lodash'
// import numeral from 'numeral'

const regx_end_session = /^Ended\sdesktop\ssession\s"(.*)"\sfrom\s(.*)\sto\s(.*),\s(\d+)\s(.*)$/
const regx_start_remote = /^Started\sremote\sdesktop\swithout\snotification\s\((.*)\)$/
const regx_start_session = /^Started\sdesktop\ssession\s"(.*)"\sfrom\s(.*)\sto\s(.*)$/

export default {
  install(Vue) {
    Vue.prototype.$getWebURL = () => {
      //return 'http://localhost:8080'
      return 'http://192.168.0.15:80'
    }
    Vue.prototype.$getJupyterURL = () => {
      //return 'http://www.naver.com'
      return 'http://192.168.137.2:39470'
    }
  }
}
