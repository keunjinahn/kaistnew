<template>
    <div :disabled="true" class="abl-img" contenteditable="false"
        @mouseenter="onMouseEnterHandler()" 
        @mouseleave="onMouseLeaveHandler()">
        <template v-if="hovered">
            <div class="abl-img-point abl-img-point-tl" @mousedown="onMouseDownHandler($event, 3)"></div>
            <div class="abl-img-point abl-img-point-tm" @mousedown="onMouseDownHandler($event, 2)"></div>
            <div class="abl-img-point abl-img-point-tr" @mousedown="onMouseDownHandler($event, 3)"></div>
            <div class="abl-img-point abl-img-point-ml" @mousedown="onMouseDownHandler($event, 1)"></div>
            <div class="abl-img-point abl-img-point-mr" @mousedown="onMouseDownHandler($event, 1)"></div>
            <div class="abl-img-point abl-img-point-bl" @mousedown="onMouseDownHandler($event, 3)"></div>
            <div class="abl-img-point abl-img-point-bm" @mousedown="onMouseDownHandler($event, 2)"></div>
            <div class="abl-img-point abl-img-point-br" @mousedown="onMouseDownHandler($event, 3)"></div>
        </template>
        <img class="attch-img" :src="path" :style="imgStyle" draggable="false" @load="onImageLoadHandler($event)">
    </div>
</template>

<script>
export default {
    props: {
        path: { type: String, require: true },
        width: { type: String, default: null },
        height: { type: String, default: null },
        disabled:{ type: Boolean, default: false },
    },
    methods: {
        onImageLoadHandler ({target}) {
            if (this.width && this.width !== 'auto') this.width = parseInt(this.width.replace('px', ''), 10)
            if (this.height && this.height !== 'auto') this.height = parseInt(this.height.replace('px', ''), 10)
            this.cwidth = this.width || target.width
            this.cheight= this.height || target.height
        },
        onMouseEnterHandler () {
            this.hovered = true
        },
        onMouseLeaveHandler () {
            this.hovered = false
        },
        onMouseUpHandler (evt) {
            console.log(`MOUSE UP ${evt.pageX} ${evt.pageY}`)
            window.onmousemove = null
            window.onmouseup = null
            this.resizing = false
        },
        onMouseMoveHandler (evt) {
            // console.log(`MOUSE MOVE ${evt.pageX} ${evt.pageY}`)
            if (this.d & 1) this.cwidth = this.w + (evt.pageX - this.x)
            if (this.d & 2) this.cheight = this.h + (evt.pageY - this.y)
        },
        onMouseDownHandler (evt, dir) {
            console.log(`MOUSE DOWN ${evt.pageX} ${evt.pageY}`)
            this.d = dir
            this.x = evt.pageX
            this.y = evt.pageY
            this.w = this.width
            this.h = this.height

            this.resizing = true
            window.onmousemove = this.onMouseMoveHandler.bind(this)
            window.onmouseup = this.onMouseUpHandler.bind(this)
        }
    },
    computed: {
        imgStyle () {
            let width = this.cwidth
            let height = this.cheight
            
            if (width) width = width + 'px' 
            else width = 'auto'

            if (height) height = height + 'px' 
            else height = 'auto'

            return {width, height}
        }
    },
    data () {
        return {
            hovered: false, resizing: false,
            d: 0, x: 0, y: 0, w: 0, h: 0, 
            cwidth: 150,
            cheight: null
        }
    }
}
</script>

<style lang="scss" scoped>

</style>