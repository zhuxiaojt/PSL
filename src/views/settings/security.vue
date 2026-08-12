<script setup>
import PSLCard from '../../components/common/PSLCard.vue'
import PSLCheckbox from '../../components/common/PSLCheckbox.vue'
const props = defineProps(['config','saveConfig'])
import { ref, watch } from 'vue'
const localConfig = ref({})

watch(() => props.config, (newConfig) => {
    localConfig.value = { ...newConfig }
}, { deep: true, immediate: true })

function clearlogs() {
    window.invoke('clear_logs');
}

function clearlogfile() {
    window.invoke('clear_log_file');
}

async function saveConfig() {
    await props.saveConfig(localConfig.value)
}
</script>
<template>
    <div class="security-container">
        <PSLCard title="扫描设置">
            <div class="security-item">
                <PSLCheckbox class="security-checkbox" v-model="localConfig.reportSuspiciousFiles" @change="saveConfig" label="报告可疑文件" />
            </div>
        </PSLCard>
        <PSLCard title="日志设置">
            <div class="security-item">
                <span class="security-label">日志显示最大条数</span>
                <input class="security-input" type="number" v-model="localConfig.maxLogs" @change="saveConfig" />
            </div>
            <div class="security-item">
                <button class="security-btn" @click="clearlogs">清除日志</button>
                <button class="security-btn-danger" @click="clearlogfile">清空日志文件</button>
            </div>
        </PSLCard>
        <PSLCard title="高级安全设置">
            <div class="security-item">
                <PSLCheckbox class="security-checkbox" v-model="localConfig.enableDefendnot" @change="saveConfig" label="接管 Windows Defender" />
            </div>
        </PSLCard>
    </div>
</template>
<style scoped>
.security-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    overflow: auto;
    padding-bottom: 15px;
}
.security-item {
    display: flex;
    align-items: center;
    margin-bottom: 15px;
}
.security-item:last-child {
    margin-bottom: 0;
}
.security-label {
    margin-right: 30px;
    font-size: 14px;
    color: #333e48;
}
.security-input {
    flex: 1;
    border-radius: 3px;
    padding: 5px 8px;
    border: 1px solid #3c96ef;
    transition: all 0.2s ease-in-out;
}
.security-input:hover {
    outline: none;
    background-color: #e3f0fd;
}
.security-input:focus {
    outline: none;
    border: 1px solid #1171cf;
    background-color: #e3f0fd;
}
.security-input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.security-btn {
    width: 140px;
    height: 35px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #333e48;
    color: #333e48;
    transition: all 0.2s ease-in-out;
}
.security-btn:hover {
    border: 1px solid #1171cf;
    color: #1171cf;
    background-color: #e3f0fd;
    transition: all 0.2s ease-in-out;
}
.security-btn-danger {
    width: 140px;
    height: 35px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #ce2111;
    color: #ce2111;
    margin-left: 20px;
    transition: all 0.2s ease-in-out;
}
.security-btn-danger:hover {
    border: 1px solid #ff4c4c;
    color: #ff4c4c;
    background-color: #fbeced;
    transition: all 0.2s ease-in-out;
}
</style>