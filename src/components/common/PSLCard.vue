<script setup>
const props = defineProps({
    title: {
        type: String,
        default: ''
    }
})
</script>
<template>
    <div class="psl-card">
        <div v-if="props.title !== ''" class="card-title">{{ props.title }}</div>
        <slot></slot>
    </div>
</template>
<style scoped>
.psl-card {
    display: flex;
    flex-direction: column;
    width: calc(100% - 60px);
    padding: 15px;
    margin-top: 15px;
    margin-left: 15px;
    margin-right: 15px;
    background-color: rgba(255, 255, 255, 0.945);
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    transition: all 0.1s ease-in-out;
}

.psl-card:hover {
    box-shadow: 0 0 5px rgba(16, 107, 199, 0.5);
}

.card-title {
    font-weight: bold;
    margin-bottom: 15px;
    transition: all 0.1s ease-in-out;
}

.psl-card:hover .card-title {
    color: #106bc7;
}
</style>