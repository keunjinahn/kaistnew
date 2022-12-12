<template>
    <div>
        <modal-alert />
        <modal-confirm />
        <modal-prompt />
    </div>
</template>

<script>
import ModalAlert from './Modal_Alert'
import ModalConfirm from './Modal_Confirm'
import ModalPrompt from './Modal_Prompt'
export default {
    components: {ModalAlert, ModalConfirm, ModalPrompt}
}
</script>