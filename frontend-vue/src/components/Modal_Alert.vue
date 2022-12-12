<template>
  <v-dialog v-model="dialog" max-width="400">
    <v-card>
      <v-card-title class="headline">{{title || '알림'}}</v-card-title>
      <v-card-text>{{text}}</v-card-text>

      <v-card-actions>
        <v-spacer/>
        <v-btn color="green darken-1" text @click="dialog = false">
          확인
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  mounted () {
    this.$session.$on('modal-alert', (text, title) => {
      this.title = title || null
      this.text = text || ''
      this.dialog = true
    })
  },
  data () {
    return {
      dialog: false,
      title: null,
      text: ''
    }
  }
}
</script>