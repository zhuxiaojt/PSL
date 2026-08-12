<template>
    <svg
        v-bind="restAttrs"
        xmlns="http://www.w3.org/2000/svg"
        :width="size"
        :height="size"
        viewBox="0 0 24 24"
        :fill="fill"
        :stroke="color"
        :stroke-width="computedStrokeWidth"
        stroke-linecap="round"
        stroke-linejoin="round"
        :class="combinedClass"
    >
        <path d="M11 22c-3.806-1.45-7-3.966-7-9V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1v4" />
        <circle cx="17.5" cy="17.5" r="3" :fill="fill" />
        <path d="M19.5 19.5L22 22" />
    </svg>
</template>

<script setup>
import { computed, useAttrs } from 'vue'

const props = defineProps({
    size: {
        type: Number,
        default: 24
    },
    color: {
        type: String,
        default: 'currentColor'
    },
    fill: {
        type: String,
        default: 'none'
    },
    'stroke-width': {
        type: Number,
        default: 2
    },
    'absolute-stroke-width': {
        type: Boolean,
        default: false
    },
    'default-class': {
        type: String,
        default: 'lucide-icon'
    }
})

const attrs = useAttrs()

const combinedClass = computed(() => {
    const defaultClass = props['default-class']
    const userClass = attrs.class || ''
    return userClass ? `${defaultClass} ${userClass}` : defaultClass
})

const computedStrokeWidth = computed(() => {
    const size = props.size || 24
    const strokeWidth = props['stroke-width'] || 2
    const absoluteStrokeWidth = props['absolute-stroke-width']
    
    if (absoluteStrokeWidth) {
        return (strokeWidth * 24) / size
    }
    
    return strokeWidth
})

const {
    class: _class,
    size: _size,
    color: _color,
    fill: _fill,
    'stroke-width': _strokeWidth,
    'absolute-stroke-width': _absoluteStrokeWidth,
    'default-class': _defaultClass,
    ...restAttrs
} = attrs
</script>