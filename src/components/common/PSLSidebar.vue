<script setup>
const props = defineProps({
    isShowingSidebarAnimation: {
        type: Boolean,
        default: false
    },
    isShowingAnimation: {
        type: Boolean,
        default: false
    },
    items: {
        type: Array,
        default: []
    },
    isActive: {
        type: Function,
        default: (page)=>{}
    },
    goto: {
        type: Function,
        default: (page)=>{}
    }
})
</script>
<template>
    <div class="left-nav" :class="{'show-animation': props.isShowingSidebarAnimation, 'item-animation': props.isShowingAnimation}">
        <div v-for="item in props.items" :key="item.page" class="nav-item" :class="{'active': props.isActive(item.page)}" @click="props.goto(item.page)">
            <component :is="item.icon" :size="20" />
            <span class="nav-item-text">{{ item.text }}</span>
        </div>
    </div>
</template>
<style scoped>
.left-nav {
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    width: 150px;
    height: calc(100% - 30px);
    background-color: rgba(255, 255, 255, 0.945);
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
    z-index: 100;
    transition: all 0.1s ease-in-out;
    padding: 15px 0;
}
.left-nav.show-animation {
    width: 300px;
    transition: all 0.1s ease-in-out;
}
.nav-item {
    opacity: 1;
    display: flex;
    align-items: center;
    border: 1px solid transparent;
    padding: 7px 15px;
    cursor: pointer;
    gap: 10px;
    transition: all 0.2s ease-in-out;
}
.nav-item-text {
    font-size: 14px;
}
.nav-item.active {
    color: #127ae1;
}
.nav-item::before {
    content: '';
    position: relative;
    width: 4px;
    height: 0px;
    opacity: 0;
    left: -15px;
    margin-right: -15px;
    margin-top: -10px;
    margin-bottom: -10px;
    background-color: #127ae1;
    border-top-right-radius: 2px;
    border-bottom-right-radius: 2px;
    transition: height 0.2s linear(0 0%,-0.1 20%, 1.1 80%, 1 100%) , opacity 0.1s ease-in-out;
}
.nav-item.active::before {
    opacity: 1;
    height: 25px;
}
.nav-item:hover {
    background-color: #e9f3fd;
    border: 1px solid #cde4fb;
}
.item-animation .nav-item {
    opacity: 0;
    transform: translateX(-10px);
}
</style>