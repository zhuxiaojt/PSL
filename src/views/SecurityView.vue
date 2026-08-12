<script setup>
import { ShieldSearch } from '../components/common/icons/index.js'
import { Ban, ShieldMinus } from '@lucide/vue'
import { ref, onMounted, shallowRef } from 'vue'
import Scan from './security/scan.vue'
import Quarantine from './security/quarantine.vue'
import PSLSidebar from '../components/common/PSLSidebar.vue'

const isShowingSidebarAnimation = ref(false)
const isShowingAnimation = ref(true)
const nowPage = ref('')
const hasAppeared = ref(false)

function onBeforeEnter(el) {
  if (!hasAppeared.value) {
    hasAppeared.value = true
    el.style.transition = 'opacity 0.2s ease-in-out, margin-top 0.2s linear(0 0%,-0.3 30%, 1.3 70%, 1 100%)'
  }
}

const items = shallowRef([
    {
        page: 'scan',
        icon: ShieldSearch,
        text: '扫描'
    },
    {
        page: 'quarantine',
        icon: Ban,
        text: '隔离区'
    },
    {
        page: 'trust',
        icon: ShieldMinus,
        text: '信任区'
    }
])

function goto(page) {
    nowPage.value = page
}

function isActive(page) {
    return nowPage.value === page
}

onMounted(() => {
    const fromPath = window.history.state?.back || ''
    if (fromPath === '/') {
        isShowingSidebarAnimation.value = true
    }
    setTimeout(() => {
        isShowingSidebarAnimation.value = false
        isShowingAnimation.value = false
        nowPage.value = 'scan'
    }, 1)
})
</script>
<template>
    <div class="security-container">
        <PSLSidebar :isShowingSidebarAnimation="isShowingSidebarAnimation" :isShowingAnimation="isShowingAnimation" :items="items" :isActive="isActive" :goto="goto" />
        <div class="security-right-container">
            <Transition name="fade" @before-enter="onBeforeEnter"> 
                <Scan class="security-right" v-if="nowPage === 'scan'" />
            </Transition>
            <Transition name="fade" @before-enter="onBeforeEnter">
                <Quarantine class="security-right" v-if="nowPage === 'quarantine'" />
            </Transition>
        </div>
    </div>
</template>
<style scoped>
.security-container {
    display: flex;
    flex-direction: row;
    height: calc(100vh - 50px);
    user-select: none;
}
.security-right-container {
    position: relative;
    width: calc(100% - 150px);
}
.security-right {
    position: absolute;
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