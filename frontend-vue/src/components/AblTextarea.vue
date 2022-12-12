<template>
  <div
    ref="editable"
    class="abl-textarea"
    v-on="listeners"
    v-bind:value="value"
    @paste ="pasteFunction"
    :style="{height,width}"
    :contenteditable="true"
  />
</template>

<script>
import Vue from 'vue'
import AblAttachImage from '@/components/AblAttachImage'

const AblAttachImageClass = Vue.extend(AblAttachImage)
export default {
  props: {
    value: { type: String, default: '' },
    height: { type: String, default: '250px' },
    width: { type: String, default: '100%' },
    disabled:{ type: Boolean, default: false },
  },
  computed: {
    listeners() {
      return { input: this.onInput, change: this.onInput, blur: this.onInput };
    },
  },
  // watch: {
  //   "value": {
  //     handler() {
  //       this.$refs.editable.innerHTML = this.value;
  //       this.setInitialValue()
  //       this.$emit('needUpdate')
  //     },
  //   }
  // },
  mounted() {
    this.$refs.editable.innerHTML = this.value;
    this.setInitialValue()
  },
  methods: {
    onInput(e) {
      this.$emit('input', e.target.innerHTML);
    },
    setInitialValue () {
      if (!this.value) return;
      let v = this.value, images = []
      v.replace(/\[=([0-9a-z-/.]+)\|(\d+px|auto)\|(\d+px|auto)\]/g, (match, path, width, height, offset) => {
        images.push({offset, path, width, height, length: match.length})
        return match
      })

      const range = document.createRange()
      let toffset = 0

      for (let imgdata of images) {
        const {offset, path, width, height, length} = imgdata
        
        const img = new AblAttachImageClass({propsData: {path, width, height}})
        img.$mount()

        let lastIndex = this.$refs.editable.childNodes.length - 1
        range.setStart(this.$refs.editable.childNodes[lastIndex], offset - toffset)
        range.setEnd(this.$refs.editable.childNodes[lastIndex], offset - toffset + length)
        toffset += (offset + length)
        range.deleteContents()
        range.insertNode(img.$el)
      }
    },
    async pasteFunction(pasteEvent, callback){
      if(pasteEvent.clipboardData == false){
          if(typeof(callback) == "function"){
              console.log('Undefined ')
              callback(undefined);
          }
      }
      //
      var items = pasteEvent.clipboardData.items;
      console.log("items :" + JSON.stringify(items))
      if(items == undefined){
          if(typeof(callback) == "function"){
              callback(undefined);
              console.log('Undefined 2')
          }
      }
      console.log("items.length :" + JSON.stringify(items.length))
      for (var i = 0; i < items.length; i++) {
          if (items[i].type.indexOf("image") == -1) continue;
          console.log("items[i] :" + JSON.stringify( items[i].getAsFile()))
          this.$emit("callBackImage", items[i].getAsFile());
      }
    }
  },
};
</script>

<style lang="scss" scoped>
.abl-textarea {
    overflow-y: auto;
    outline: none;
    &:hover, &:focus {
        background-color: #ebebeb;
    }

}
</style>
