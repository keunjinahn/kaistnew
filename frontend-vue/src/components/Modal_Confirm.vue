<template>
  <v-dialog v-model="dialog" max-width="290">
    <v-card>
      <v-card-title class="headline">{{title || '알림'}}</v-card-title>
      <v-card-text>{{text}}</v-card-text>

      <v-card-actions>
        <v-spacer/>
        <v-btn color="primary darken-1" dark @click="submit">
          확인
        </v-btn>
        <v-btn color="primary darken-1" text @click="dialog = false">
          취소
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  methods: {
    submit () {
      if (typeof this.cb === 'function') this.cb(true)
      this.dialog = false
    }
  },
  mounted () {
    this.$session.$on('modal-confirm', (text, title, cb) => {
      this.title = title || null
      this.text = text || ''
      this.dialog = true
      this.cb = cb
    })
  },
  data () {
    return {
      dialog: false,
      title: null,
      text: '',
      cb: () => {}
    }
  }
}
</script>