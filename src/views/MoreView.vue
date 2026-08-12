<script setup>
import { Info } from '@lucide/vue'
import { ref, onMounted } from 'vue'
import PSLSidebar from '../components/common/PSLSidebar.vue'
import About from './more/about.vue'

const isShowingSidebarAnimation = ref(false)
const isShowingAnimation = ref(true)
const nowPage = ref('')

const items = ref([
    {
        icon: Info,
        text: '关于',
        page: 'about'
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
        nowPage.value = 'about'
    }, 1)
})
</script>
<template>
    <div class="more-container">
        <PSLSidebar :isShowingSidebarAnimation="isShowingSidebarAnimation" :isShowingAnimation="isShowingAnimation" :items="items" :isActive="isActive" :goto="goto" />
        <Transition name="fade"> 
            <About v-if="nowPage === 'about'" />
        </Transition>
    </div>
</template>
<style scoped>
.more-container {
    display: flex;
    flex-direction: row;
    height: calc(100vh - 50px);
    user-select: none;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease-in-out, margin-top 0.2s linear(0 0%,-0.3 30%, 1.3 70%, 1 100%);
}
.fade-enter-from,
.fade-leave-to {
    margin-top: -20px;
    opacity: 0;
}
</style>