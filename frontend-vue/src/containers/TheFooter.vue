<template>
  <CFooter :fixed="false">
    <div>
      <a href="http://NeuralTech.com/" target="_blank" style="margin-left:20px">(주)뉴럴테크</a>
      <span class="ml-1">&copy; {{new Date().getFullYear()}} NeuralTech Corp. All rights reserved..</span>
    </div>
    <div class="mfs-auto">
<!--      <span class="mr-1" target="_blank">Powered by</span>-->
<!--      <a href="https://coreui.io/vue">CoreUI for Vue</a>-->
    </div>
  </CFooter>
</template>

<script>
export default {
  name: 'TheFooter'
}
</script>
