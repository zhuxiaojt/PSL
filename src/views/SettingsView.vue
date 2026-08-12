<script setup>
import { Shield, Shirt, Loader2 } from '@lucide/vue'
import { ref, onMounted, toRaw } from 'vue'
import PSLSidebar from '../components/common/PSLSidebar.vue'
import Security from './settings/security.vue'
import Individuation from './settings/individuation.vue'

const isShowingSidebarAnimation = ref(false)
const isShowingAnimation = ref(true)
const nowPage = ref('')
const config = ref({ unloaded: true })
const hasAppeared = ref(false)

const items = ref([
    {
        icon: Shield,
        text: '安全设置',
        page: 'security'
    },
    {
        icon: Shirt,
        text: '个性化',
        page: 'individuation'
    }
])

function goto(page) {
    nowPage.value = page
}

function isActive(page) {
    return nowPage.value === page
}

async function saveConfig(newConfig) {
    console.log(toRaw(newConfig))
    window.invoke('save_config', JSON.stringify(toRaw(newConfig)))
    config.value = JSON.parse(await window.invoke('get_config'));
    window.dispatchEvent(new CustomEvent('psl-config-updated'));
}
function onBeforeEnter(el) {
  if (!hasAppeared.value) {
    hasAppeared.value = true
    el.style.transition = 'opacity 0.2s ease-in-out, margin-top 0.2s linear(0 0%,-0.3 30%, 1.3 70%, 1 100%)'
  }
}
onMounted(async() => {
    const fromPath = window.history.state?.back || ''
    if (fromPath === '/') {
        isShowingSidebarAnimation.value = true
    }
    setTimeout(() => {
        isShowingSidebarAnimation.value = false
        isShowingAnimation.value = false
        nowPage.value = 'security'
    }, 1)
    config.value = JSON.parse(await window.invoke('get_config'));
    config.value.reportSuspiciousFiles = config.value.reportSuspiciousFiles ?? true
    config.value.enableDefendnot = config.value.enableDefendnot ?? false
    config.value.titleBar = config.value.titleBar ?? 'default'
    config.value.maxLogs = config.value.maxLogs ?? 100
    console.log(config.value)
})
</script>
<template>
    <div class="settings-container">
        <PSLSidebar :isShowingSidebarAnimation="isShowingSidebarAnimation" :isShowingAnimation="isShowingAnimation" :items="items" :isActive="isActive" :goto="goto" />
        <div class="settings-right-container">
            <div class="loader-frame" v-if="config.unloaded">
                <Loader2 :size="50" class="loader" />
            </div>
            <Transition name="fade" @beforeEnter="onBeforeEnter"> 
                <Security v-if="nowPage === 'security' && !config.unloaded" :config="config" :saveConfig="saveConfig" class="settings-right" />
            </Transition>
            <Transition name="fade" @beforeEnter="onBeforeEnter">
                <Individuation v-if="nowPage === 'individuation' && !config.unloaded" :config="config" :saveConfig="saveConfig" class="settings-right" />
            </Transition>
        </div>
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
.settings-container {
    display: flex;
    flex-direction: row;
    height: calc(100vh - 50px);
    user-select: none;
}
.settings-right-container {
    display: flex;
    position: relative;
    width: calc(100% - 150px);
    height: calc(100vh - 50px);
    user-select: none;
}
.settings-right {
    position: absolute;
    width: 100%;
    height: 100%;
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