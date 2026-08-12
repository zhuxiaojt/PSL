<script setup>
import { Zap, HardDrive, Folder } from '@lucide/vue'
import PSLCard from '../../../components/common/PSLCard.vue'
const props = defineProps(['reload'])
function fastscan(){
    window.invoke('fast_scan');
}
function diskscan(){
    window.invoke('disk_scan');
}
function customscan(){
    window.invoke('custom_folder_scan');
}
</script>
<template>
    <div class="scan-container">
        <PSLCard title="扫描">
            <div class="scan-card-container" @click="fastscan">
                <div class="dom-placeholder" />
                <div class="scan-card-background">
                    <Zap class="scan-logo" />
                    <div class="scan-content">
                        <div class="scan-name">快速扫描</div>
                        <div class="scan-gray">快速扫描系统敏感区域</div>
                    </div>
                </div>
            </div>
            <div class="scan-card-container" @click="diskscan">
                <div class="dom-placeholder" />
                <div class="scan-card-background">
                    <HardDrive class="scan-logo" />
                    <div class="scan-content">
                        <div class="scan-name">全盘扫描</div>
                        <div class="scan-gray">扫描系统所有区域</div>
                    </div>
                </div>
            </div>
            <div class="scan-card-container" @click="customscan">
                <div class="dom-placeholder" />
                <div class="scan-card-background">
                    <Folder class="scan-logo" />
                    <div class="scan-content">
                        <div class="scan-name">自定义扫描</div>
                        <div class="scan-gray">自定义扫描的区域</div>
                    </div>
                </div>
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
.scan-card-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    height: 60px;
}
.scan-card-background { 
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    border: 1px solid transparent;
    border-radius: 5px;
    margin: 10px;
    padding: 0;
    transition: all 0.1s ease-in-out;
}
.scan-card-container:hover .scan-card-background {
    margin: 0;
    padding: 10px;
    background-color: #eaf4fe;
    border-color:#d2e6fb;
}
.scan-logo {
    width: 30px;
    height: 30px;
    margin-right: 15px;
}
.scan-content {
    display: flex;
    flex-direction: column;
}
.scan-gray {
    font-size: 12px;
    color: #666666;
}
</style>