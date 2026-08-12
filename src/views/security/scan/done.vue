<script setup>
import PSLCard from '../../../components/common/PSLCard.vue'
import { Check } from '@lucide/vue';
const props = defineProps(['reload', 'scan_status'])
function closescan(){
    window.invoke('close_scan');
}
function quarantine_files(){
    window.invoke('quarantine_files');
}
</script>
<template>
    <div class="scan-container">
        <PSLCard title="扫描完成">
            <div v-if="props.scan_status.suspicious_files.length != 0 || props.scan_status.malicious_files.length != 0">
                <span class="scan-gray">
                    共扫描 {{ props.scan_status.scanned_file_count }} 个文件，发现 {{ props.scan_status.malicious_files.length + props.scan_status.suspicious_files.length }} 个威胁
                </span>
                <div v-for="file in props.scan_status.malicious_files" :key="file" class="malicious_file">
                    <div class="malicious_tag">恶意</div>
                    {{ file }}
                </div>
                <div v-for="file in props.scan_status.suspicious_files" :key="file" class="suspicious_file">
                    <div class="suspicious_tag">可疑</div>
                    {{ file }}
                </div>
            </div>
            <div v-if="props.scan_status.suspicious_files.length != 0 || props.scan_status.malicious_files.length != 0" class="done-card-container">
                <button class="do-btn" v-if="props.scan_status.doing_quarantine.length == 0" @click="quarantine_files">立即处理</button>
                <button class="disabled-btn" v-if="props.scan_status.doing_quarantine.length != 0" disabled>处理中...</button>
                <button class="close-btn" @click="closescan">暂不处理</button>
            </div>
            <div v-if="props.scan_status.suspicious_files.length == 0 && props.scan_status.malicious_files.length == 0" class="no-malicious-card">
                <span class="no-malicious-left"><Check class="scan-logo" /><div class="no-malicious-content">电脑很安全，没有发现威胁<span class="scan-gray">共扫描 {{ props.scan_status.scanned_file_count }} 个文件</span></div></span>
                <button class="close-btn" @click="closescan">返回</button>
            </div>
        </PSLCard>
    </div>
</template>
<style scoped>
.scan-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    overflow: auto;
    padding-bottom: 15px;
}
.no-malicious-content {
    display: flex;
    flex-direction: column;
}
.scan-gray {
    font-size: 12px;
    color: #666666;
}
.do-btn {
    width: 140px;
    height: 35px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #1171cf;
    color: #1171cf;
    transition: all 0.2s ease-in-out;
    margin-right: 20px;
}
.disabled-btn {
    width: 140px;
    height: 35px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #a6a6a6;
    color: #a6a6a6;
    transition: all 0.2s ease-in-out;
    margin-right: 20px;
}
.close-btn {
    width: 140px;
    height: 35px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #333e48;
    color: #333e48;
    transition: all 0.2s ease-in-out;
}
.close-btn:hover,
.do-btn:hover {
    border: 1px solid #1171cf;
    color: #1171cf;
    background-color: #e3f0fd;
    transition: all 0.2s ease-in-out;
}
.malicious_file,
.suspicious_file {
    font-size: 12px;
    overflow-wrap: break-word;
    word-break: break-all;
    white-space: normal;
    padding: 10px 0;
    border-bottom: 1px solid #dddddd;
    display: flex;
    flex-direction: row;
    align-items: center;
}
.malicious_file:last-child,
.suspicious_file:last-child {
    border-bottom: none;
}
.malicious_tag {
    flex-shrink: 0;
    height: 18px;
    width: 25px;
    color: #ff0000;
    border: 1px solid #ff0000;
    padding: 3px 5px;
    border-radius: 5px;
    margin-right: 10px;
}
.suspicious_tag {
    flex-shrink: 0;
    height: 18px;
    width: 25px;
    color: #ffd900;
    border: 1px solid #ffd900;
    padding: 3px 5px;
    border-radius: 5px;
    margin-right: 10px;
}
.no-malicious-card {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}
.no-malicious-left {
    display: flex;
    flex-direction: row;
    align-items: center;
}
.scan-logo {
    width: 50px;
    height: 50px;
    margin-right: 5px;
}
</style>