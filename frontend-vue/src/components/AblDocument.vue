<template>
    <div class="abl-doc elevation-3">
        <div class="abl-doc-inner" ref="doc">
            <slot />
        </div>
    </div>
</template>

<script>
import html2canvas from 'html2canvas'
export default {
    methods: {
        async capture (width=1000,height=1500) {
            await this.$nextTick()
            width = this.$refs.doc.clientWidth + 10
            height = this.$refs.doc.clientHeight
            console.log(`capture / width: ${width}, height: ${height}`)

            this.canvas = await html2canvas(this.$refs.doc, {width: width, height: height})
            let blob = this.canvas.toDataURL('image/png')
            return blob
        },
        getDocumentSize () {
            const size = [0, 0]
            if (!this.$refs.doc) return size
            size[0] = this.$refs.doc.clientWidth
            size[1] = this.$refs.doc.clientHeight
            return size
        }
    },
    mounted () {
        this.$emit('mounted')
    },
    data () {
        return {
            canvas: null
        }
    }
}
</script>

<style lang="scss" scoped>
.abl-doc {
    width: 1000px;
    border-radius: 3px;
    background-color: white;
}
.abl-doc-inner {
    padding: 0px;
    background-color: white;
}
.abl-doc-header {
    display: flex;
    justify-content: space-between;
    border-bottom: 3px double #a0a0a0;
    padding: 5px 0;

    .top-logo { height: 30px; }
}

.abl-doc-title {
    position: relative;
    padding: 25px 0 20px;
    text-align: center;
    .tmpl-no {
        position: absolute;
        top: 2px; left: 2px;
    }
    .tmpl-no-1 {
        position: absolute;
        top: 2px; left: 2px;
        text-align: center;
    }
    .title-text {
        font-size: 20px;
        border-collapse: collapse;
        border-bottom: 1px solid #a0a0a0;
        font-weight: normal;
        color: black;
        text-align: center;
    }
}

.abl-doc-sign {
    padding: 10px 0 20px;
}

.abl-doc-footer {
    display: flex;
    justify-content: space-between;
    border-top: 3px double #a0a0a0;
    padding: 5px 0;

    .footer-logo { height: 30px; }
}


.abl-table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid #a0a0a0;
    color:black;
    th, td {
        padding: 1px 1px;
        border: 1px solid #a0a0a0;
        font-size: 14px;
    }

    .m-h { background-color: #ebebeb; }
    .s-h { background-color: #ebebeb;}
    .w-h { background-color: #ffffff; }
    .dbl-t { border-top: 3px double #a0a0a0; }
    .dbl-b { border-bottom: 3px double #a0a0a0; }
    .area-a { width: 80% !important;}
    .textarea-context {
        display: flex;
        min-height: 280px;
    }
    .s-h-1 {float:left;background-color: #ebebeb;border-right: 1px solid #a0a0a0;width:50%;height:200px!important;line-height: 30px;padding-top: 65px;}
    .s-h-2 {float:right;background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:50%;height:100px!important;line-height: 30px;}
    .s-h-3-1 {background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:100%;height:100%!important;}
    .s-h-3-2 {background-color: #ebebeb;width:100%;height:100%!important;}
    .s-h-4 {float:left;background-color: white;border-right: 1px solid #a0a0a0;width:50%;height:240px!important;}
    .s-h-4-0 {float:left;background-color: white;border-right: 0px solid #a0a0a0;width:50%;height:240px!important;}
    .s-h-4-1 {background-color: white;border-bottom: 1px solid #a0a0a0;width:100%;height:30px!important;}
    .s-h-4-2 {background-color: white;border-bottom: 0px solid #a0a0a0;width:100%;height:60px!important;}
}
.abl-table-ts {
    width: 100%;
    border-collapse: collapse;
    border-top: 1.5px solid #333333;
    border-bottom: 1.5px solid #333333;
    font-family: "돋움체";
    font-weight: normal;
    font-size: 12px;
    color:black;
    tr {
      border-bottom: 1px solid #333333;
    }
    th {
        padding: 0px 0px;
        background-color: #bbbbbb;
        border: 1px solid #a0a0a0;
        font-weight: normal;
    }
    td {
        padding: 0px 0px;
        border: 1px solid #a0a0a0;
        text-align: center;
    }
    .m-h { background-color: #ebebeb; }
    .s-h { background-color: #ebebeb;}
    .w-h { background-color: #ffffff; }
    .dbl-t { border-top: 3px double #a0a0a0; }
    .dbl-b { border-bottom: 3px double #a0a0a0; }
    .area-a { width: 80% !important;}
    .textarea-context {
        display: flex;
        min-height: 280px;
    }
    .s-h-1 {float:left;background-color: #ebebeb;border-right: 1px solid #a0a0a0;width:50%;height:200px!important;line-height: 30px;padding-top: 65px;}
    .s-h-2 {float:right;background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:50%;height:100px!important;line-height: 30px;}
    .s-h-3-1 {background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:100%;height:100%!important;}
    .s-h-3-2 {background-color: #ebebeb;width:100%;height:100%!important;}
    .s-h-4 {float:left;background-color: white;border-right: 1px solid #a0a0a0;width:50%;height:240px!important;}
    .s-h-4-0 {float:left;background-color: white;border-right: 0px solid #a0a0a0;width:50%;height:240px!important;}
    .s-h-4-1 {background-color: white;border-bottom: 1px solid #a0a0a0;width:100%;height:30px!important;}
    .s-h-4-2 {background-color: white;border-bottom: 0px solid #a0a0a0;width:100%;height:60px!important;}
}
.abl-table-empty {
    width: 100%;
    border-collapse: collapse;
    border-bottom: 1px solid #a0a0a0;
    font-family: "돋움체";
    font-weight: normal;
    font-size: 12px;
    color:black;
    th, td {
        padding: 0px 0px;
        border: 0px solid #a0a0a0;
        font-weight: normal;
    }
    .s-t-blank {
        background-color: #ffffff;
        border: 0px solid #a0a0a0;
    }
    .m-h { background-color: #ebebeb; }
    .s-h { background-color: #ebebeb;}
    .w-h { background-color: #ffffff; }
    .dbl-t { border-top: 3px double #a0a0a0; }
    .dbl-b { border-bottom: 3px double #a0a0a0; }
    .area-a { width: 80% !important;}
    .textarea-context {
        display: flex;
        min-height: 280px;
    }
    .s-h-1 {float:left;background-color: #ebebeb;border-right: 1px solid #a0a0a0;width:50%;height:200px!important;line-height: 30px;padding-top: 65px;}
    .s-h-2 {float:right;background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:50%;height:100px!important;line-height: 30px;}
    .s-h-3-1 {background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:100%;height:100%!important;}
    .s-h-3-2 {background-color: #ebebeb;width:100%;height:100%!important;}
    .s-h-4 {float:left;background-color: white;border-right: 1px solid #a0a0a0;width:50%;height:240px!important;}
    .s-h-4-0 {float:left;background-color: white;border-right: 0px solid #a0a0a0;width:50%;height:240px!important;}
    .s-h-4-1 {background-color: white;border-bottom: 1px solid #a0a0a0;width:100%;height:30px!important;}
    .s-h-4-2 {background-color: white;border-bottom: 0px solid #a0a0a0;width:100%;height:60px!important;}
}
.abl-table-subtitle {
    width: 100%;
    border-collapse: collapse;
    font-family: "돋움체";
    font-weight: normal;
    font-size: 12px;
    color:black;
}
.abl-table2 {
    width: 100%;
    border-collapse: collapse;
    border: 0px solid #a0a0a0;

    th, td {
        padding: 5px 5px;
        border: 0px solid #a0a0a0;
        border-bottom: 1px solid #a0a0a0;
        height: 30px;
    }

    .m-h { background-color: #ebebeb; }
    .s-h { background-color: #ebebeb;}
    .w-h { background-color: #ffffff; }
    .dbl-t { border-top: 0px double #a0a0a0; }
    .dbl-b { border-bottom: 0px double #a0a0a0; }
    .area-a { width: 80% !important;}
    .textarea-context {
        display: flex;
        min-height: 280px;
    }
    .s-h-1 {float:left;background-color: #ebebeb;border-right: 1px solid #a0a0a0;width:50%;height:200px!important;line-height: 30px;padding-top: 65px;}
    .s-h-2 {float:right;background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:50%;height:100px!important;line-height: 30px;}
    .s-h-3-1 {background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:100%;height:100%!important;}
    .s-h-3-2 {background-color: #ebebeb;width:100%;height:100%!important;}
    .s-h-4 {float:left;background-color: white;border-right: 1px solid #a0a0a0;width:50%;height:240px!important;}
    .s-h-4-0 {float:left;background-color: white;border-right: 0px solid #a0a0a0;width:50%;height:240px!important;}
    .s-h-4-1 {background-color: white;border-bottom: 1px solid #a0a0a0;width:100%;height:30px!important;}
    .s-h-4-2 {background-color: white;border-bottom: 0px solid #a0a0a0;width:100%;height:60px!important;}

}
.abl-textarea {
    width: 100%;
    outline: none;
    resize: none;

    &:hover, &:focus {
        background-color: #ebebeb;
    }
}

.abl-input {
    width: 100%;
    outline: none;
    margin-left: 10px;
    &:hover, &:focus {
        background-color: #ebebeb;
    }
}

.abl-input_w {
    width: 100%;
    outline: none;
    text-align: center;
    &:hover, &:focus {
        background-color: #ffffff;
    }
}
.my-class {
    background-color: #0d47a1;
}
.abl-table-sitemap {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid #a0a0a0;
  color:black;
  font-weight: normal;
  th, td {
    padding: 1px 1px;
    border: 1px solid #a0a0a0;
    font-size: 12px;
  }

  .m-h { background-color: #ebebeb; }
  .s-h { background-color: #ebebeb;height:30px;}
  .w-h { background-color: #ffffff; }
  .dbl-t { border-top: 3px double #a0a0a0; }
  .dbl-b { border-bottom: 3px double #a0a0a0; }
  .area-a { width: 80% !important;}
  .textarea-context {
    display: flex;
    min-height: 280px;
  }
  .s-h-1 {float:left;background-color: #ebebeb;border-right: 1px solid #a0a0a0;width:50%;height:200px!important;line-height: 30px;padding-top: 65px;}
  .s-h-2 {float:right;background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:50%;height:100px!important;line-height: 30px;}
  .s-h-3-1 {background-color: #ebebeb;border-bottom: 1px solid #a0a0a0;width:100%;height:100%!important;}
  .s-h-3-2 {background-color: #ebebeb;width:100%;height:100%!important;}
  .s-h-4 {float:left;background-color: white;border-right: 1px solid #a0a0a0;width:50%;height:240px!important;}
  .s-h-4-0 {float:left;background-color: white;border-right: 0px solid #a0a0a0;width:50%;height:240px!important;}
  .s-h-4-1 {background-color: white;border-bottom: 1px solid #a0a0a0;width:100%;height:30px!important;}
  .s-h-4-2 {background-color: white;border-bottom: 0px solid #a0a0a0;width:100%;height:60px!important;}
}

</style>
