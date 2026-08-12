<script setup>
import { Circle, Dot } from '@lucide/vue'
const props = defineProps(['modelValue', 'lineWidth', 'items'])
const emit = defineEmits(['update:modelValue', 'change'])
</script>
<template>
    <div class="psl-choose-box">
        <div class="psl-choose-line" v-for="line in Math.ceil(props.items.length / props.lineWidth)" :key="line">
            <div class="choose-item" v-for="item in props.items.slice((line - 1) * props.lineWidth, line * props.lineWidth)" :key="item.id" :style="{'line-height': props.lineWidth + 'px', 'width': 100 / props.lineWidth + '%'}" @click="emit('update:modelValue', item.id); emit('change')" :class="{ 'checked': item.id === props.modelValue }">
                <Circle class="choose-icon" :class="{ 'checked-icon': item.id === props.modelValue }" >
                    <Transition name="fade">
                        <Dot v-if="item.id === props.modelValue" stroke-width="8" class="choose-icon-inner" />
                    </Transition>
                </Circle>
                {{ item.name }}
            </div>
        </div>
    </div>
</template>
<style scoped>
@keyframes checked-icon-pop-in {
    0% {
        transform: scale(0.5);
    }
    50% {
        transform: scale(1.1);
    }
    100% {
        transform: scale(1);
    }
}
.psl-choose-box {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.psl-choose-line {
    display: flex;
    width: 100%;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
}
.choose-icon {
    width: 20px;
    height: 20px;
    margin-right: 5px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
}
.checked .choose-icon {
    color: #0f64b8;
}
.choose-icon-inner {
    color: #0f64b8;
    transition: all 0.2s ease;
    transform-origin: center center;
}
.choose-item {
    font-size: 14px;
    color: #333e48;
    display: flex;
    flex-direction: row;
    align-items: center;
    transition: all 0.2s ease;
}
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease, transform 0.2s linear(0 0%,-0.3 30%, 1.3 70%, 1 100%);
}
.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: scale(0.5);
}
.checked-icon {
    animation: checked-icon-pop-in 0.2s ease-in-out;
}
.choose-item:hover {
    color:#127ae1;
}
.choose-item:hover .choose-icon {
    color: #127ae1;
}
.choose-item:hover .choose-icon-inner {
    color: #127ae1;
}
</style>