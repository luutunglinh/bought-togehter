import {createApp, h} from 'vue/dist/vue.esm-bundler';
import 'ant-design-vue/dist/antd.css';
import ShopifyFrontend from './ShopifyFrontend.vue'
import Antd from "ant-design-vue";
import './main.css';
var app = createApp({
    name: 'App',
    render: () => {
        return <ShopifyFrontend/>
    }
})
app.use(Antd).mount('#app-storefront')

