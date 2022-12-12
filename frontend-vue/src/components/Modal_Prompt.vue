<template>
  <v-dialog v-model="dialog" max-width="290">
    <v-card>
      <v-card-title class="headline">{{title || '입력'}}</v-card-title>
      <v-card-text>
        <div>{{text}}</div>
        <div>
          <v-text-field
            v-model="userInput"
            :rules="rules"
            :counter="counter"
            outlined dense
          />
        </div>
      </v-card-text>

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
      if (!this.userInput) return;
      if (typeof this.cb === 'function') this.cb(this.userInput)
      this.dialog = false
    }
  },
  mounted () {
    this.$session.$on('modal-prompt', (text, options, cb) => {
      this.title = options.title || null
      this.text = text || ''
      this.counter = options.counter || false
      this.rules = options.rules || []
      this.userInput = ''
      this.dialog = true
      this.cb = cb
    })
  },
  data () {
    return {
      dialog: false,
      title: null,
      text: '',
      userInput: '',
      counter: false,
      rules: [],
      cb: () => {}
    }
  }
}
</script>