<script setup>
import PSLCard from '../../components/common/PSLCard.vue'
import PSLModal from '../../components/common/PSLModal.vue'
import { onMounted, ref } from 'vue'
const quarantine = ref({})
const isDeleteModalVisible = ref(false)
const isRestoreModalVisible = ref(false)
const deletingFile = ref('')
const restoringFile = ref('')
function showDeleteModal(file) {
    deletingFile.value = file
    isDeleteModalVisible.value = true
}
function deleteQuarantinedFile() {
    window.invoke('delete_quarantined_file', deletingFile.value)
    isDeleteModalVisible.value = false
    reloadQuarantine()
}
function closeDeleteModal() {
    isDeleteModalVisible.value = false
}
function showRestoreModal(file) {
    restoringFile.value = file
    isRestoreModalVisible.value = true
}
function restoreQuarantinedFile() {
    window.invoke('restore_quarantined_file', restoringFile.value)
    isRestoreModalVisible.value = false
    reloadQuarantine()
}
function closeRestoreModal() {
    isRestoreModalVisible.value = false
}
async function reloadQuarantine() {
    quarantine.value = JSON.parse(await window.invoke('get_quarantined_files'))
}
onMounted(async () => {
    await reloadQuarantine();
})
</script>
<template>
    <PSLCard title="隔离区">
        <Transition name="modal-fade">
            <PSLModal v-if="isDeleteModalVisible" title="确认删除"
                :content="`确定要永久删除文件：\n ${quarantine[deletingFile]} \n\n确认后将无法恢复`" :isDanger="true"
                :buttons="[{ 'id': 'confirm', 'label': '确认', 'onclick': deleteQuarantinedFile }, { 'id': 'cancel', 'label': '取消', 'onclick': closeDeleteModal }]" />
        </Transition>
        <Transition name="modal-fade">
            <PSLModal v-if="isRestoreModalVisible" title="确认恢复"
                :content="`确定要恢复文件：\n ${quarantine[restoringFile]} \n\n这是一个病毒文件，恢复后可能会导致系统风险`" :isDanger="false"
                :buttons="[{ 'id': 'confirm', 'label': '确认', 'onclick': restoreQuarantinedFile }, { 'id': 'cancel', 'label': '取消', 'onclick': closeRestoreModal }]" />
        </Transition>
        <div v-for="(value, key) in quarantine" :key="key" class="quarantine-item">
            {{ value }}
            <div class="quarantine-btn-container">
                <button class="restore-btn" @click="showRestoreModal(key)">恢复</button>
                <button class="delete-btn" @click="showDeleteModal(key)">删除</button>
            </div>
        </div>
        <span v-if="Object.keys(quarantine).length == 0" class="quarantine-gray">
            没有隔离的文件
        </span>
    </PSLCard>
</template>
<style scoped>
.quarantine-item {
    font-size: 12px;
    overflow-wrap: break-word;
    word-break: break-all;
    white-space: normal;
    padding: 10px 0;
    border-bottom: 1px solid #dddddd;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}

.quarantine-item:last-child {
    border-bottom: none;
}

.quarantine-gray {
    font-size: 12px;
    color: #666666;
}

.quarantine-btn-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin-left: 20px;
}

.restore-btn {
    width: 140px;
    height: 35px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #333e48;
    color: #333e48;
    transition: all 0.2s ease-in-out;
}

.restore-btn:hover {
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
</style>
