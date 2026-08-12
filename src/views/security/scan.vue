<script setup>
import Home from './scan/home.vue'
import Scanning from './scan/scanning.vue'
import Done from './scan/done.vue'
import { Loader2 } from '@lucide/vue'
import { onMounted, onUnmounted, ref } from 'vue'
const scan_status = ref({ status: 'unknown' })
const isUnmounted = ref(false)
const hasAppeared = ref(false)
async function reload(){
    if(isUnmounted.value){
        return;
    }
    scan_status.value = JSON.parse(await window.invoke('query_scan_status'));
    setTimeout(reload,200)
}
function onBeforeEnter(el) {
  if (!hasAppeared.value) {
    hasAppeared.value = true
    el.style.transition = 'opacity 0.2s ease-in-out, margin-top 0.2s linear(0 0%,-0.3 30%, 1.3 70%, 1 100%)'
  }
}
onMounted(async() => {
    await reload();
})
onUnmounted(() => {
    isUnmounted.value = true;
})
</script>
<template>
    <div class="scan-main-container">
        <div class="loader-frame" v-if="scan_status.status == 'unknown'">
            <Loader2 :size="50" class="loader" />
        </div>
        <Transition name="fade" @before-enter="onBeforeEnter">
            <Home v-if="scan_status.status == 'unstarted'" :reload="reload" class="scan-view" />
        </Transition>
        <Transition name="fade" @before-enter="onBeforeEnter">
            <Scanning v-if="scan_status.status == 'scanning'" :reload="reload" :scan_status="scan_status" class="scan-view" />
        </Transition>
        <Transition name="fade" @before-enter="onBeforeEnter">
            <Done v-if="scan_status.status == 'done'" :reload="reload" :scan_status="scan_status" class="scan-view" />
        </Transition>
    </div>
</template>
<style scoped>
@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
.scan-main-container{
    position: relative;
    width: 100%;
    height: 100%;
    overflow: auto;
}
.scan-view{
    position: absolute;
}
.loader-frame {
    color: #ffffff;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.loader {
    animation: spin 2s linear infinite;
}
.fade-leave-active {
    transition: opacity 0.2s ease-in-out, margin-top 0.2s linear(0 0%,-0.3 30%, 1.3 70%, 1 100%);
}
.fade-enter-active {
    transition: opacity 0.2s ease-in-out 0.2s, margin-top 0.2s linear(0 0%,-0.3 30%, 1.3 70%, 1 100%) 0.2s;
}
.fade-enter-from,
.fade-leave-to {
    margin-top: -20px;
    opacity: 0;
}
</style>