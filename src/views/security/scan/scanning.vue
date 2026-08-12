<script setup>
import PSLCard from '../../../components/common/PSLCard.vue'
const props = defineProps(['reload', 'scan_status'])
</script>
<template>
    <div class="scan-container">
        <PSLCard title="扫描中">
            <div class="process-bar">
                <div class="process-value" :style="{ width: props.scan_status.process + '%' }" />
            </div>
            <div class="scanning-card-container">
                <span class="scan-process">{{ props.scan_status.process }}%</span>
                <span class="scan-gray scanning-file">正在扫描：{{ props.scan_status.scanning_file }}</span>
            </div>
        </PSLCard>
        <PSLCard title="已发现的威胁">
            <div v-for="file in props.scan_status.malicious_files" :key="file" class="malicious_file">
                <div class="malicious_tag">恶意</div>
                {{ file }}
            </div>
            <div v-for="file in props.scan_status.suspicious_files" :key="file" class="suspicious_file">
                <div class="suspicious_tag">可疑</div>
                {{ file }}
            </div>
            <span v-if="props.scan_status.suspicious_files.length == 0 && props.scan_status.malicious_files.length == 0" class="scan-gray">
                暂未发现威胁
            </span>
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
.scan-process {
    font-size: 12px;
    color: #106bc7;
    margin-right: 5px;
}
.scan-gray {
    font-size: 12px;
    color: #666666;
}
.process-bar {
    width:100%;
    background: #dddddd;
    height: 4px;
    border-radius: 2px;
}
.process-value {
    background: #106bc7;
    height: 4px;
    border-radius: 2px;
    transition: all 0.2s ease-in-out;
}
.scanning-file {
    overflow-wrap: break-word;
    word-break: break-all;
    white-space: normal;
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
</style>