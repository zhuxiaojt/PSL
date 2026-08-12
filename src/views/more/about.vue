<script setup>
import { Hexagon } from '@lucide/vue'
import { Python, Vue } from '../../components/common/icons/index.js'
import PSLCard from '../../components/common/PSLCard.vue'
</script>
<template>
    <div class="about-container">
        <PSLCard title="关于">
            <div class="about-card-container">
                <img src="../../assets/logo.png" alt="PSL" class="about-logo">
                <div class="about-content">
                    <div class="about-title">Power Security Layer (PSL)</div>
                    <span class="about-version">当前版本：1.0.0</span>
                </div>
            </div>
        </PSLCard>
        <PSLCard title="鸣谢与声明">
            <div class="about-card-container">
                <img src="https://pcl2.aoe.top/favicon.ico" class="about-logo">
                <div class="about-content">
                    <div class="about-title">PCL2</div>
                    <span class="about-version">PSL参考了PCL2的UI设计。</span>
                </div>
            </div>
            <div class="about-card-container">
                <img src="https://lucide.dev/favicon.ico" class="about-logo">
                <div class="about-content">
                    <div class="about-title">Lucide Icons</div>
                    <span class="about-version">PSL使用了Lucide Icons作为图标库。部分自制图标参考了Lucide的设计风格。</span>
                </div>
            </div>
            <div class="about-card-container">
                <img src="https://bbs.kafan.cn/favicon.ico" class="about-logo">
                <div class="about-content">
                    <div class="about-title">卡饭论坛</div>
                    <span class="about-version">PSL的AI模型使用卡饭论坛下载的样本进行训练。</span>
                </div>
            </div>
        </PSLCard>
        <PSLCard title="软件架构">
            <div class="about-card-container">
                <Hexagon class="about-logo node-logo" />
                <div class="about-content">
                    <div class="about-title">窗口服务</div>
                    <span class="about-version">Node.js</span>
                </div>
            </div>
            <div class="about-card-container">
                <Python class="about-logo python-logo" />
                <div class="about-content">
                    <div class="about-title">后端</div>
                    <span class="about-version">Python</span>
                </div>
            </div>
            <div class="about-card-container">
                <Vue class="about-logo vue-logo" />
                <div class="about-content">
                    <div class="about-title">前端</div>
                    <span class="about-version">Vue.js</span>
                </div>
            </div>
        </PSLCard>
    </div>
</template>
<style scoped>
.about-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    overflow: auto;
    padding-bottom: 15px;
}
.about-card-container {
    display: flex;
    flex-direction: row;
    align-items: center;
    width: 100%;
    margin-bottom: 5px;
}
.about-logo {
    width: 30px;
    height: 30px;
    margin-right: 15px;
}
.node-logo {
    color:#5FA04E;
}
.python-logo {
    color:#3776AB;
}
.vue-logo {
    color:#4FC08D;
}
.about-content {
    display: flex;
    flex-direction: column;
}
.about-version {
    font-size: 12px;
    color: #666666;
}
</style>