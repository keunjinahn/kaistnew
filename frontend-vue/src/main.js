import 'core-js/stable'
import Vue from 'vue'
import App from './App'
import router from './router'
import CoreuiVue from '@coreui/vue'
import { iconsSet as icons } from './assets/icons/icons.js'
import store from './store'
import Session from './plugins/session.js'
import vuetify from './plugins/vuetify'
import HighchartsVue from 'highcharts-vue'
import utils from './plugins/utils';
import moment from 'moment'
import VueMoment from 'vue-moment'
import Constant from './plugins/constant.js';
Vue.use(VueMoment, { moment })
Vue.config.performance = true
Vue.use(CoreuiVue)
Vue.prototype.$log = console.log.bind(console)
Vue.use(Session)
Vue.use(HighchartsVue)
Vue.use(utils)
Vue.use(Constant)
Vue.prototype.$constant = Constant
new Vue({
  el: '#app',
  router,
  store,
  vuetify,
  HighchartsVue,
  icons,
  template: '<App/>',
  components: {
    App
  }
})
