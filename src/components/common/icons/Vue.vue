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
	    <path d="M 22.2675 3.1274 L 12.0002 20.9482 L 1.7330 3.1274 M 17.3825 3.1274 L 12.0002 12.2763 L 6.6180 3.1274" />
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