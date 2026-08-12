<script setup>
import { Home, ShieldCheck, Bolt, LayoutGrid, Minus,X } from '@lucide/vue'
import { useRouter } from 'vue-router'
import { onMounted, ref } from 'vue'

const config = ref({titleBar: 'default'})
const titleBarPictureBase64 = ref('')

const router = useRouter()

function isActive(path) {
    return router.currentRoute.value.path === path
}

function goto(path) {
    router.push(path);
}

function closeApp() {
    window.invoke("close");
}
function minimizeApp() {
    window.minimize();
}

onMounted(async () => {
    config.value = JSON.parse(await window.invoke('get_config'))
    config.value.titleBar = config.value.titleBar ?? 'default'
    config.value.titleBarOnLeft = config.value.titleBarOnLeft ?? false
    if (config.value.titleBar === 'picture') {
        config.value.titleBarPicture = config.value.titleBarPicture
        titleBarPictureBase64.value = await window.invoke('get_picture_base64', config.value.titleBarPicture)
    }
    window.addEventListener('psl-config-updated', async () => {
        config.value = JSON.parse(await window.invoke('get_config'))
        config.value.titleBar = config.value.titleBar ?? 'default'
        config.value.titleBarOnLeft = config.value.titleBarOnLeft ?? false
        if (config.value.titleBar === 'picture') {
            config.value.titleBarPicture = config.value.titleBarPicture
            titleBarPictureBase64.value = await window.invoke('get_picture_base64', config.value.titleBarPicture)
        }
    })
    document.addEventListener('contextmenu', (e) => {
        e.preventDefault();
    })
    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey && e.key == 'r')||(e.key == 'F5')) {
            e.preventDefault();
        }
    });
})
</script>
<template>
    <div class="top-nav" nexfep-auto-drag>
        <div v-if="!config.titleBarOnLeft || config.titleBar !== 'none'" class="title">
            <span v-if="config.titleBar === 'default'">PSL</span>
            <span v-if="config.titleBar === 'text'">{{ config.titleBarText }}</span>
            <img v-if="config.titleBar === 'picture'" :src="`data:image/png;base64,${titleBarPictureBase64}`"  class="title-img" />
        </div>
        <div class="nav">
            <div class="nav-item" :class="{'active': isActive('/')}" @click="goto('/')" nexfep-no-drag>
                <Home size="18" />
                <span>主页</span>
            </div>
            <div class="nav-item" :class="{'active': isActive('/security')}" @click="goto('/security')" nexfep-no-drag>
                <ShieldCheck size="18" />
                <span>安全</span>
            </div>
            <div class="nav-item" :class="{'active': isActive('/settings')}" @click="goto('/settings')" nexfep-no-drag>
                <Bolt size="18" />
                <span>设置</span>
            </div>
            <div class="nav-item" :class="{'active': isActive('/more')}" @click="goto('/more')" nexfep-no-drag>
                <LayoutGrid size="18" />
                <span>更多</span>
            </div>
        </div>
        <div class="control-btn-container">
            <div class="control-btn" @click="minimizeApp" nexfep-no-drag>
                <Minus size="21" />
            </div>
            <div class="control-btn" @click="closeApp" nexfep-no-drag>
                <X size="21" />
            </div>
        </div>
    </div>
    <router-view class="container" />
</template>
<style scoped>
.top-nav {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 50px;
    padding: 0 10px;
    background-color: #106bc7;
    z-index: 1000;
    user-select: none;
}
.title {
    color: #ffffff;
    margin-left: 10px;
    font-size: 20px;
    width: 61px;
    white-space: nowrap;
    display: flex;
    align-items: center;
}
.title-img {
    height: 35px;
}
.control-btn-container {
    display: flex;
    flex-direction: row;
    width: 61px;
    gap: 5px;
}
.control-btn {
    cursor: pointer;
    color: #ffffff;
    border-radius: 14px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 28px;
    height: 28px;
    transition: all 0.2s ease-in-out;
}
.control-btn:hover {
    background-color: #3c8ee0;
}
.nav {
    display: flex;
    flex-direction: row;
    gap: 10px;
}
.nav-item {
    cursor: pointer;
    color: #ffffff;
    border-radius: 14px;
    display: flex;
    justify-content: center;
    align-items: center;
    width: 78px;
    height: 28px;
    font-size: 13px;
    gap: 5px;
    transition: all 0.2s ease-in-out;
}
.nav-item:hover {
    background-color: #3c8ee0;
}
.nav-item.active {
    background-color: #ffffff;
    color: #127ae1;
}
.container {
    height: calc(100vh - 50px);
    background: linear-gradient(45deg, #dbdbf0 0%, #cce9f5 100%);
}
</style>