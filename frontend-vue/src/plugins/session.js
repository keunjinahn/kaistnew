import _ from 'lodash'
import Vue from 'vue'
import axios from 'axios'
import constant from './constant'


const $http = axios.create({ baseURL: '/api/v1/' })
const session = new Vue({
    methods: {
        delay (ms) {
            return new Promise((resolve) => {
                setTimeout(() => {
                    resolve()
                }, ms)
            })
        },
        async setToken (user) {
            $http.defaults.headers.common['token'] = user.token
            sessionStorage.setItem('user', JSON.stringify(user))
            this.authorized = true
            this.user = user
        },
        unsetToken () {
            delete $http.defaults.headers.common['token']
            sessionStorage.removeItem('user')
            this.authorized = false
            this.user = null
        },
        async logout() {
            this.$session.unsetToken()
            await this.$http.post('logout')
            sessionStorage.setItem('user','')
            sessionStorage.setItem('sessionToken', '')
            this.authorized = false
            this.$router.push('/login').catch(()=>{});
            location.reload(true)
        },
        getUserId() {
            let user = JSON.parse(sessionStorage.getItem('user'))
            if(user != undefined)
                return user.user_id
            return null
        },
        getUserName() {
            let user = JSON.parse(sessionStorage.getItem('user'))
            if(user != undefined)
                return user.user_name
            return null
        },
        getUserIndex() {
            let user = JSON.parse(sessionStorage.getItem('user'))
            if(user != undefined)
                return user.id
            return null
        },
        getUserInfo() {
            let user = JSON.parse(sessionStorage.getItem('user'))
            if(user != undefined)
                return user
            return null
        },
        getUserType() {
            let user = JSON.parse(sessionStorage.getItem('user'))
            if(user != undefined)
                return user.user_type
            return null
        },
        setSearchString(search_string){
            this.search_string = search_string
        },
        getSearchString(){
            return this.search_string
        },
        check_permission(){
            if(this.authorized){
                return true
            }
            return false
        },
    },
    created () {
        let user = JSON.parse(sessionStorage.getItem('user'))
        if (user) this.setToken(user)
    },
    data () {
        return {
            authorized: false,
            search_string:''
        }
    }
})

export default {
    install (Main) {
        Main.prototype.$http = $http
        Main.prototype.$session = session
        Main.prototype.CONSTANT = constant
    }
}