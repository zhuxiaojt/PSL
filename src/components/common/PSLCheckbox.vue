<script setup>
import { Check } from '@lucide/vue'
const props = defineProps(['modelValue', 'label'])
const emit = defineEmits(['update:modelValue', 'change'])
</script>
<template>
    <div class="psl-checkbox-container" @click="emit('update:modelValue', !props.modelValue); emit('change')">
       <div class="psl-checkbox-main-container" :class="{'checked': props.modelValue, 'unchecked': !props.modelValue }">
            <Transition name="fade">
                <Check v-if="props.modelValue" class="psl-checkbox-icon" />
            </Transition>
        </div>
        <span class="psl-checkbox-label">{{ props.label }}</span>
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
@keyframes checked-icon-pop-out {
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
.psl-checkbox-container {
    display: inline-flex;
    flex-direction: row;
    align-items: center;
    width: auto;
}
.psl-checkbox-main-container {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 16px;
    height: 16px;
    border: 1px solid #333e48;
    border-radius: 4px;
    transition: all 0.2s ease;
}
.psl-checkbox-icon {
    width: 14px;
    height: 14px;
    stroke-width: 3px;
    color: #0f64b8;
    transition: all 0.2s ease;
}
.checked {
    border-color: #0f64b8;
    animation: checked-icon-pop-in 0.2s ease-in-out;
}
.unchecked {
    animation: checked-icon-pop-out 0.2s ease-in-out;
}
.psl-checkbox-container:hover .psl-checkbox-main-container {
    border-color: #127ae1;
}
.psl-checkbox-container:hover .psl-checkbox-icon {
    color: #127ae1;
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
.psl-checkbox-label {
    font-size: 14px;
    color: #333e48;
    transition: all 0.2s ease;
    margin-left: 8px;
}
.psl-checkbox-container:hover .psl-checkbox-label {
    color: #127ae1;
}
</style>
