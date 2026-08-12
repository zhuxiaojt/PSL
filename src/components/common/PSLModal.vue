<script setup>
const props = defineProps(['title', 'content', 'isDanger', 'buttons']);
</script>
<template>
    <div class="psl-modal-background" :class="{'danger': props.isDanger }" nexfep-auto-drag>
        <div class="psl-modal-container" nexfep-no-drag>
            <span class="psl-modal-title" :class="{'danger': props.isDanger }">{{ props.title }}</span>
            <span class="psl-modal-content">{{ props.content }}</span>
            <div class="psl-modal-btn-container">
                <button v-for="btn in props.buttons" :key="btn.id" class="psl-modal-btn" :class="{'danger': props.isDanger }" @click="btn.onclick">{{ btn.label }}</button>
            </div>
        </div>
    </div>
</template>
<style scoped>
@keyframes modal-pop-in {
    0% {
        opacity: 0.3;
        transform: translateY(50px) rotate(-1.5deg);
        transform-origin: center center;
    }
    20% {
        transform: translateY(40px) rotate(-3deg);
        transform-origin: center center;
    }
    60% {
        transform: translateY(-15px) rotate(3deg);
        transform-origin: center center;
    }
    70% {
        transform: translateY(-7px) rotate(-1.5deg);
        transform-origin: center center;
    }
    80% {
        transform: translateY(-3px) rotate(-1.5deg);
        transform-origin: center center;
    }
    100% {
        opacity: 1;
        transform: translateY(0px) rotate(0deg);
        transform-origin: center center;
    }
}
.psl-modal-background {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}
.psl-modal-background.danger {
    background-color: rgba(80, 0, 0, 0.6);
}
.psl-modal-container {
    animation: modal-pop-in 0.4s ease;
    background-color: #fff;
    min-width: 300px;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
}
.psl-modal-title {
    color: #0f64b8;
    font-size: 23px;
    padding-left: 10px;
    padding-right: 10px;
    padding-bottom: 10px;
    margin-bottom: 10px;
    border-bottom: 2px solid #0f64b8;
}
.psl-modal-title.danger {
    color: #ff4c4c;
    border-bottom: 2px solid #ff4c4c;
}
.psl-modal-content {
    font-size: 14px;
    padding-left: 10px;
    padding-right: 10px;
    margin-bottom: 20px;
    white-space: pre-wrap;
    color: #5c5c5c
}
.psl-modal-btn-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: flex-end;
    gap: 10px;
}
.psl-modal-btn {
    width: 50px;
    height: 30px;
    background-color: transparent;
    border-radius: 3px;
    border: 1px solid #333e48;
    color: #333e48;
    transition: all 0.2s ease-in-out;
}
.psl-modal-btn:first-child {
    border: 1px solid #1171cf;
    color: #1171cf;
}
.psl-modal-btn.danger:first-child {
    border: 1px solid #ce2111;
    color: #ce2111;
}
.psl-modal-btn:hover {
    border: 1px solid #1171cf;
    color: #1171cf;
    background-color: #e3f0fd;
}
.psl-modal-btn.danger:first-child:hover {
    border: 1px solid #ff4c4c;
    color: #ff4c4c;
    background-color: #fbeced;
}
.modal-fade-enter-active, 
.modal-fade-leave-active {
    transition: all 0.2s ease-in-out;
}
.modal-fade-enter-from {
    background-color: rgba(0, 0, 0, 0) !important;
}
.modal-fade-enter-from.danger {
    background-color: rgba(80, 0, 0, 0) !important;
}
.modal-fade-leave-to {
    opacity: 0;
}
</style>