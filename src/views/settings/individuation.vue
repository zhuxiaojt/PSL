<script setup>
import PSLCard from '../../components/common/PSLCard.vue'
import PSLCheckBox from '../../components/common/PSLCheckBox.vue'
import PSLChooseBox from '../../components/common/PSLChooseBox.vue'
const props = defineProps(['config','saveConfig'])
import { ref, watch } from 'vue'
const localConfig = ref({})
const titleBarItems = ref([
    { id: 'none', name: '无' },
    { id: 'default', name: '默认' },
    { id: 'text', name: '文本' },
    { id: 'picture', name: '图片' }
])
const choosePicture = async () => {
    const picture = await window.invoke('choose_picture')
    if (picture) {
        localConfig.value.titleBarPicture = picture
        saveConfig()
    }
}
const deletePicture = () => {
    localConfig.value.titleBarPicture = undefined
    localConfig.value.titleBar = 'default'
    saveConfig()
}
watch(() => props.config, (newConfig) => {
    localConfig.value = { ...newConfig }
}, { deep: true, immediate: true })

async function saveConfig() {
    if (localConfig.value.titleBar === 'picture') {
        if (!localConfig.value.titleBarPicture) {
            await choosePicture()
            if (!localConfig.value.titleBarPicture) {
                localConfig.value.titleBar = props.config.titleBar
                return;
            }
        }
    }
    await props.saveConfig(localConfig.value)
}
</script>
<template>
    <div class="preference-container">
        <PSLCard title="标题栏" class="preference-card">
            <div class="preference-item">
                <PSLChooseBox class="preference-choosebox" v-model="localConfig.titleBar" @change="saveConfig" :items="titleBarItems" :lineWidth="4" />
            </div>
            <div class="preference-item">
                <PSLCheckBox v-if="localConfig.titleBar === 'none'" class="preference-checkbox preference-optional-item" v-model="localConfig.titleBarOnLeft" @change="saveConfig" label="标题栏居左" />
                <div class="preference-input-frame preference-optional-item" v-if="localConfig.titleBar === 'text'">
                    <span class="preference-input-label">标题栏文本</span>
                    <input class="preference-input" v-model="localConfig.titleBarText" @change="saveConfig" />
                </div>
                <div class="preference-input-frame preference-optional-item" v-if="localConfig.titleBar === 'picture'">
                    <button class="preference-button change-btn" @click="choosePicture">更改图片</button>
                    <button class="preference-button delete-btn" @click="deletePicture">清空图片</button>
                </div>
            </div>
        </PSLCard>
    </div>
</template>
<style scoped>
.preference-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    overflow: auto;
    padding-bottom: 15px;
}
.preference-optional-item {
    margin-top: 15px;
}
.preference-input-frame {
    width: 100%;
    display: flex;
    flex-direction: row;
    align-items: center;
}
.preference-input-label {
    margin-right: 30px;
    font-size: 14px;
    color: #333e48;
}
.preference-input {
    flex: 1;
    border-radius: 3px;
    padding: 5px 8px;
    border: 1px solid #3c96ef;
    transition: all 0.2s ease-in-out;
}
.preference-input:hover {
    outline: none;
    background-color: #e3f0fd;
}
.preference-input:focus {
    outline: none;
    border: 1px solid #1171cf;
    background-color: #e3f0fd;
}
.change-btn {
    width: 140px;
    height: 35px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #333e48;
    color: #333e48;
    transition: all 0.2s ease-in-out;
}
.change-btn:hover {
    border: 1px solid #1171cf;
    color: #1171cf;
    background-color: #e3f0fd;
    transition: all 0.2s ease-in-out;
}
.delete-btn {
    width: 140px;
    height: 35px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #ce2111;
    color: #ce2111;
    margin-left: 20px;
    transition: all 0.2s ease-in-out;
}
.delete-btn:hover {
    border: 1px solid #ff4c4c;
    color: #ff4c4c;
    background-color: #fbeced;
    transition: all 0.2s ease-in-out;
}
.optional-fade-enter-active, .optional-fade-leave-active {
    transition: all 0.2s ease-in-out;
}
.optional-fade-enter-from, .optional-fade-leave-to {
    opacity: 0;
}
</style>