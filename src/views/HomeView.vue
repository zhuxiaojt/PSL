<script setup>
import { ShieldCheck, ShieldX, ShieldAlert } from '@lucide/vue';
import { computed, onMounted, onUnmounted, ref, toRaw } from 'vue'
import { useRouter } from 'vue-router'
import PSLCard from '../components/common/PSLCard.vue';

const isShowingAnimation = ref(true)
const isTurnedMain = ref(false)
const isUnmounted = ref(false)
const isSafely = ref(1)
const router = useRouter()
const logs = ref('Loading...')
const isHitokotoCooling = ref(false)
const hitokoto = ref({
    hitokoto: 'Loading...'
})

function fastscan(){
    window.invoke('fast_scan');
    router.push('security')
}

async function getlogs(){
    if(isUnmounted.value){
        return;
    }
    logs.value = await window.invoke('get_logs');
    setTimeout(getlogs, 500);
}

async function getHitokoto(){
    if(isHitokotoCooling.value){
        return;
    }
    isHitokotoCooling.value = true;
    hitokoto.value = { hitokoto: 'Loading...' }
    hitokoto.value = await (await fetch('https://v1.hitokoto.cn/')).json()
    setTimeout(() => {
        isHitokotoCooling.value = false;
    }, 2000);
}

onMounted(() => {
    getlogs();
    getHitokoto();
    setTimeout(() => {
        isShowingAnimation.value = false
        isTurnedMain.value = true
    }, 1)
})
onUnmounted(() => {
    isUnmounted.value = true
})
</script>
<template>
    <div class="home-container">
        <div class="home-left" :class="{'show-animation': isShowingAnimation}">
            <div class="left-content" :class="{'show-animation': isShowingAnimation}" v-if="isSafely === 1">
                <ShieldCheck size="64" />
                <span>你的电脑似乎很安全</span>
            </div>
            <div class="left-content warning" :class="{'show-animation': isShowingAnimation}" v-if="isSafely === 0">
                <ShieldAlert size="64" />
                <span>保护存在缺陷</span>
            </div>
            <div class="left-content danger" :class="{'show-animation': isShowingAnimation}" v-if="isSafely === -1">
                <ShieldX size="64" />
                <span>保护存在严重缺陷</span>
            </div>
            <div class="left-bottom" :class="{'show-animation': isShowingAnimation}">
                <button class="bottom-primary-btn" @click="fastscan">快速扫描</button>
            </div>
        </div>
        <Transition name="fade">
            <div v-if="isTurnedMain" class="home-right">
                <PSLCard title="一言">
                    <div class="hitokoto" @click="getHitokoto" :title="isHitokotoCooling?'冷却中':'点击刷新'">
                        <span class="hitokoto-span">
                            {{ hitokoto.hitokoto }}
                        </span>
                        <span v-if="hitokoto.from" class="hitokoto-from">
                            —— {{ hitokoto.from }}
                        </span>
                    </div>
                </PSLCard>
                <PSLCard title="日志">
                    <span class="logs-content">
                        {{ logs }}
                    </span>
                </PSLCard>
            </div>
        </Transition>
    </div>
</template>
<style scoped>
.home-container {
    display: flex;
    flex-direction: row;
    height: calc(100vh - 50px);
    user-select: none;
}
.home-left {
    width: 300px;
    height: 100%;
    background-color: rgba(255, 255, 255, 0.945);
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    z-index: 100;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transition: all 0.1s ease-in-out;
}
.home-left.show-animation {
    width: 100px;
    transition: all 0.1s ease-in-out;
}
.left-content {
    opacity: 1;
    width: 300px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    color: #5692cc;
    transition: all 0.2s ease-in-out 50ms;
    margin: auto 0;
    gap: 10px;
}
.left-content.warning {
    color: #ff9900;
}
.left-content.danger {
    color: #ff4c4c;
}
.left-content.show-animation {
    opacity: 0;
    transform: translateX(-50px);
    transition: all 0.2s ease-in-out 50ms;
}
.left-bottom {
    opacity: 1;
    height: auto;
    margin-bottom: 20px;
    margin-left: 0px;
    transition: all 0.2s ease-in-out 50ms;
}
.left-bottom.show-animation {
    opacity: 0;
    transform: translateX(-50px);
    transition: all 0.2s ease-in-out 50ms;
}
.bottom-primary-btn {
    width: 270px;
    height: 50px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #1171cf;
    color: #1171cf;
    transition: all 0.2s ease-in-out;
}
.bottom-primary-btn:hover {
    background-color: #e3f0fd;
    transition: all 0.2s ease-in-out;
}
.home-right {
    flex: 1;
    height: calc(100% - 15px);
    overflow: auto;
    padding-bottom: 15px;
}
.hitokoto {
    display: flex;
    flex-direction: column;
    transition: all 0.2s ease-in-out;
    padding: 5px;
}
.hitokoto-span {
    font-size: 14px;
}
.hitokoto-from {
    margin-left: auto;
    font-size: 12px;
    color: #666666;
}
.logs-content {
    padding: 10px;
    border: 1px solid #dddddd;
    border-radius: 3px;
    font-size: 14px;
    font-family: Consolas, Menlo, 'Courier New', 
                 'PingFang SC', 'Microsoft YaHei', 'Hiragino Sans GB', 
                 sans-serif;
    overflow-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
    user-select: text;
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