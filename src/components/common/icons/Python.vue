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
	    <path d="M 13.0184 3 C 15.3048 3.0001 17.11 4.8014 17.2098 7.093 C 17.2098 9 17 12 12 12 C 10 12 6 12 6.2514 16.9776 M 21.2705 11.3754 V 12.7738 M 6.4839 7.1199 H 10 H 9.1818 H 7.0214 M 17.0091 17.1174 H 11.729 M 21.2705 12.7738 C 21.2705 15.1809 19.3794 17.1008 17.0091 17.1174 C 17.1437 17.4506 17.2201 17.8139 17.2201 18.086 C 17.2201 19.6724 15.9323 20.9602 14.3157 20.9602 H 10.5036 C 8.2285 20.9602 6.3748 19.1782 6.2514 16.9776 C 4.249 16.6145 2.7375 14.8765 2.7375 12.7738 V 11.3754 C 2.7375 9.1872 4.3676 7.3843 6.4839 7.1199 C 6.3267 6.7585 6.238 6.3597 6.238 5.9429 C 6.238 4.3203 7.5593 3 9.1818 3 H 13.0184 M 17.2098 7.093 C 19.4725 7.2134 21.2705 9.0829 21.2705 11.3754" />
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