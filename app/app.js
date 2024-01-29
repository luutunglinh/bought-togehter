import {createApp, h} from 'vue/dist/vue.esm-bundler';
import App from './App.vue'
import 'ant-design-vue/dist/antd.css';
import Antd from 'ant-design-vue';
import './main.css';
var app = createApp({
    name: 'App',
    render: () => {
        return <App/>
    }
})
app.mount('#sample-app')

