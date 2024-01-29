<template>
  <div class="main-comp">
    <div class="settings-title">
      <div class="header_name_store">
        <span>Customization</span>
		<div class="selection_customization">
			<Select
				@change="handleChange"
			    v-model:value="value"
				placeholder="Select a person"
				style="width: 200px"
				:options="options"
				:default-value="options[0].value"
			></Select>
		</div>
      </div>
      <div class="header_btn_store">
        <button @click="discardProduct" class="btn btn-cancel">Discard</button>
        <button @click="saveProduct" class="btn btn-next">Save</button>
      </div>
    </div>
    <div class="custom-main">
      <div class="custom-main-left">
        <div class="custom-left-box">
          <div class="custom-title">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="12"
              height="12"
              viewBox="0 0 12 12"
              fill="none"
            >
              <g clip-path="url(#clip0_3_7364)">
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M0 6C0 2.6865 2.6865 0 6 0C9.3135 0 12 2.6865 12 6C12 9.3135 9.3135 12 6 12C2.6865 12 0 9.3135 0 6ZM6.67501 7.20115H5.39337V7.11654C5.39992 5.93719 5.68836 5.76447 6.21774 5.44746C6.27369 5.41396 6.33232 5.37885 6.3936 5.34077C6.83188 5.06548 7.16874 4.71775 7.16874 4.21065C7.16874 3.64197 6.72322 3.27251 6.16903 3.27251C5.6583 3.27251 5.1748 3.51123 5.1422 4.1922H3.78223C3.81845 2.81578 4.90852 2.1 6.17627 2.1C7.55994 2.1 8.51256 2.96825 8.51256 4.19254C8.51256 5.02202 8.09601 5.56534 7.42954 5.96378C7.37879 5.99491 7.33125 6.02353 7.28673 6.05034C6.81326 6.33539 6.68163 6.41464 6.67501 7.11654V7.20115ZM6.77747 9.00841C6.77384 9.45031 6.40801 9.80528 5.98059 9.80528C5.53869 9.80528 5.18009 9.45031 5.18372 9.00841C5.18009 8.57375 5.53869 8.21877 5.98059 8.21877C6.40801 8.21877 6.77384 8.57375 6.77747 9.00841Z"
                  fill="#5C5F62"
                />
              </g>
              <defs>
                <clipPath id="clip0_3_7364">
                  <rect width="12" height="12" fill="white" />
                </clipPath>
              </defs>
            </svg>
            <span>General Configuration</span>
          </div>
		  <div class="custom-control">
			<div class="custom-control-input">
				<span> Widget Title</span>
				<Input class="input-widget" v-model:value="widget_title"/>
			</div>
			<div class="custom-control-2col">
				<div class="custom-control-color">
					<span>Title color</span>
				  <div>
					<input type="color" v-model="title_color">
					{{ title_color }}
				  </div>
				</div>
				<div class="custom-control-number">
					<span>Title font size (px)</span>
					<InputNumber  :min="18" :max="38" v-model:value="title_font_size"/>
				</div>
			</div>
		  </div>

		  <div class="custom-control">
			<div class="custom-control-input">
				<span> Widget description</span>
				<Input v-model:value="widget_description"/>
			</div>
			<div class="custom-control-2col">
				<div class="custom-control-color">
					<span>Description color</span>
				  <div>
					<input type="color" v-model="description_color">
					{{ description_color }}
				  </div>
				</div>
				<div class="custom-control-number">
					<span>Description font size (px)</span>
					<InputNumber  :min="14" :max="38" v-model:value="description_font_size"/>
				</div>
			</div>
		  </div>  
        </div>


		<div class="custom-left-box">
          <div class="custom-title">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="12"
              height="12"
              viewBox="0 0 12 12"
              fill="none"
            >
              <g clip-path="url(#clip0_3_7364)">
                <path
                  fill-rule="evenodd"
                  clip-rule="evenodd"
                  d="M0 6C0 2.6865 2.6865 0 6 0C9.3135 0 12 2.6865 12 6C12 9.3135 9.3135 12 6 12C2.6865 12 0 9.3135 0 6ZM6.67501 7.20115H5.39337V7.11654C5.39992 5.93719 5.68836 5.76447 6.21774 5.44746C6.27369 5.41396 6.33232 5.37885 6.3936 5.34077C6.83188 5.06548 7.16874 4.71775 7.16874 4.21065C7.16874 3.64197 6.72322 3.27251 6.16903 3.27251C5.6583 3.27251 5.1748 3.51123 5.1422 4.1922H3.78223C3.81845 2.81578 4.90852 2.1 6.17627 2.1C7.55994 2.1 8.51256 2.96825 8.51256 4.19254C8.51256 5.02202 8.09601 5.56534 7.42954 5.96378C7.37879 5.99491 7.33125 6.02353 7.28673 6.05034C6.81326 6.33539 6.68163 6.41464 6.67501 7.11654V7.20115ZM6.77747 9.00841C6.77384 9.45031 6.40801 9.80528 5.98059 9.80528C5.53869 9.80528 5.18009 9.45031 5.18372 9.00841C5.18009 8.57375 5.53869 8.21877 5.98059 8.21877C6.40801 8.21877 6.77384 8.57375 6.77747 9.00841Z"
                  fill="#5C5F62"
                />
              </g>
              <defs>
                <clipPath id="clip0_3_7364">
                  <rect width="12" height="12" fill="white" />
                </clipPath>
              </defs>
            </svg>
            <span>Button Configuration</span>
          </div>
		  <div class="custom-control">
			<div class="custom-control-input">
				<span> Button Text</span>
				<Input v-model:value="btn_text"/>
			</div>
			<div class="custom-control-2col">
				<div class="custom-control-color">
					<span>Button text color</span>
				  <div>
					<input type="color" v-model="text_color">
					{{ text_color }}
				  </div>
				</div>
				<div class="custom-control-color">
					<span>Button background color (px)</span>
						<div>
						<input type="color" v-model="background_color">
						{{ background_color }}
						</div>
				</div>
				<!-- <div class="custom-control-number">
					<span>Button background color (px)</span>
					<Input  :min="18" :max="38" v-model="background_color"/>
					{{ background_color }}
				</div> -->
			</div>
			<div class="custom-control-1col">
				<span>Button border color</span>
				<div>
					<input type="color" v-model="border_color">
				{{ border_color }}
				</div>
			</div>
		  </div>  
        </div>
      </div>
      <div class="custom-main-right">
		<div class="custom-title">
			<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 12 12" fill="none">
			  <g clip-path="url(#clip0_3_7364)">
				<path fill-rule="evenodd" clip-rule="evenodd"
					  d="M0 6C0 2.6865 2.6865 0 6 0C9.3135 0 12 2.6865 12 6C12 9.3135 9.3135 12 6 12C2.6865 12 0 9.3135 0 6ZM6.67501 7.20115H5.39337V7.11654C5.39992 5.93719 5.68836 5.76447 6.21774 5.44746C6.27369 5.41396 6.33232 5.37885 6.3936 5.34077C6.83188 5.06548 7.16874 4.71775 7.16874 4.21065C7.16874 3.64197 6.72322 3.27251 6.16903 3.27251C5.6583 3.27251 5.1748 3.51123 5.1422 4.1922H3.78223C3.81845 2.81578 4.90852 2.1 6.17627 2.1C7.55994 2.1 8.51256 2.96825 8.51256 4.19254C8.51256 5.02202 8.09601 5.56534 7.42954 5.96378C7.37879 5.99491 7.33125 6.02353 7.28673 6.05034C6.81326 6.33539 6.68163 6.41464 6.67501 7.11654V7.20115ZM6.77747 9.00841C6.77384 9.45031 6.40801 9.80528 5.98059 9.80528C5.53869 9.80528 5.18009 9.45031 5.18372 9.00841C5.18009 8.57375 5.53869 8.21877 5.98059 8.21877C6.40801 8.21877 6.77384 8.57375 6.77747 9.00841Z"
					  fill="#5C5F62"/>
			  </g>
			  <defs>
				<clipPath id="clip0_3_7364">
				  <rect width="12" height="12" fill="white"/>
				</clipPath>
			  </defs>
			</svg>
			<span>Preview</span>
		</div>

		<!-- preview -->	
		<div class="preview">
			<Preview 
				:title_color ="title_color"
				:title_font_size="title_font_size"
				:widget_title = "widget_title"
				:description_color = "description_color"
				:description_font_size = "description_font_size"
				:widget_description = "widget_description"
				:background_color = "background_color"
				:border_color = "border_color"
				:text_color = "text_color"
				:btn_text = "btn_text"
				:data = "data"
			>
			</Preview>
		</div>
	  </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import Preview from "./Preview.vue";
import { Input, InputNumber ,Checkbox, Select } from "ant-design-vue";
export default {
  name: "Customization",
  components: {
    Input,
	Preview,
	Checkbox,
	InputNumber,
	Select,
  },
  created (){
	this.getCustomiazation()

  },
  data() {
    return {
		value: "",
		widget_description: 'Goods deals only for you',
      	widget_title: 'YOU MAY ALSO LIKE...',
		title_color: '#000000',
      	description_color: '#000000',
      	description_font_size: '14',
		title_font_size: '20',
		background_color: '#000000',
		border_color: '#000000',	
		btn_text: 'Buy now',
		text_color: '#FFFFFF',
		data: [
			// {
			// 	"key":47209634136359,
			// 	"name":"The Out of Stock Snowboard",
			// 	"url":"https://cdn.shopify.com/s/files/1/0846/3096/2471/products/Main_f44a9605-cd62-464d-b095-d45cdaa0d0d7.jpg?v=1701309460",
			// 	"price":"886",
			// 	"compare":null,
			// 	"quantity":10,
			// 	"isActive": true,
			// },
			// {
			// 	"key":47209634201895,
			// 	"name":"The Collection Snowboard: Hydrogen",
			// 	"url":"https://cdn.shopify.com/s/files/1/0846/3096/2471/products/Main_0a40b01b-5021-48c1-80d1-aa8ab4876d3d.jpg?v=1701309460",
			// 	"price":"600",
			// 	"compare":null,
			// 	"quantity":40,
			// 	"isActive": true,
			// },
			// {
			// 	"key":47209634660647,
			// 	"name":"The Compare at Price Snowboard",
			// 	"url":"https://cdn.shopify.com/s/files/1/0846/3096/2471/products/snowboard_sky.png?v=1701309460",
			// 	"price":"786",
			// 	"compare":"886",
			// 	"quantity":9,
			// 	"isActive": true,
			// },
		],
		data_stores: window.app_settings.stores,
	};
  },
  computed: {
	options() {
		const activeStores = this.data_stores.filter(item => item.status)
		console.log(activeStores)
		return activeStores.length > 0 ? activeStores.map(store => ({
			label: store.name,
			value: store.key,
		})) : []
	}
  },
  methods: {
	async getCustomiazation(){
		const url = "/sample-app/get_customization"
		await axios.post(url, {
			jsonrpc: "2.0",
			params: {
				'user_id': window.app_settings.id,
			},
		}).then(res =>{
			console.log(res);
			//sent data to server using Parse to JSON -> OBJECT
			const data = JSON.parse(res.data.result)
			this.title_color = data.title_color
			this.title_font_size = data.title_font_size
			this.widget_title = data.widget_title
			this.widget_description = data.widget_description
			this.description_color = data.description_color
			this.description_font_size = data.description_font_size
			this.background_color = data.background_color
			this.border_color = data.border_color
			this.text_color = data.text_color
			this.btn_text = data.btn_text
		})
	},

	async saveProduct(){
		let data = {
			"title_color": this.title_color,
			"title_font_size": this.title_font_size,
			"widget_title": this.widget_title,
			"description_color": this.description_color,
			"description_font_size": this.description_font_size,
			"widget_description": this.widget_description,
			"background_color": this.background_color,
			"border_color": this.border_color,
			"text_color": this.text_color,
			"btn_text": this.btn_text,
		}
		const url = "/sample-app/save_customization"
		await axios.post(url,{
			jsonrpc: "2.0",
			params: {
				'name': 'test',
				'data': JSON.stringify(data),
				'user_id': window.app_settings.id,
			},
		})
	},
	async handleChange(value){
		window.app_settings.store = value
		console.log("runnnnn");
		const url = '/sample-app/get_widget_data'
		await axios.post(url,{
			jsonrpc:  "2.0",
			params: {
				'shop': window.app_settings.store,
				'shop_id': 6,
				'type': 'recommendation'
			}
		}).then(res => {
			console.log('getDataCustomization',res.data.result);
			this.data = res.data.result.map(item=> ({...item, isActive: true}))

	})
	}

  },
};
</script>

<style lang="css" scoped>
.main-comp .settings-title {
  display: flex;
  width: 100%;
  justify-content: space-between;
  align-items: center;
}

.header_name_store {
	display: flex;
}

.header_name_store > span {
  color: #000;
  font-size: 20px;
  font-style: normal;
  font-weight: 600;
  line-height: 22px;


}

.main-comp > .settings-title > div {
  justify-content: center;
  align-items: center;
  gap: 12px;
}

.btn-next {
  gap: 4px;
  width: 62px;
  height: 32px;
  color: white;
  font-weight: 700;
  border: #1d1e21;
  background: #1d1e21;
}

.btn-cancel {
  font-weight: 500;
  border: #e2e2e2;
  flex: none;
  order: 1;
  flex-grow: 0;
  width: 71px;
  height: 32px;
  background: #fff;
  margin-right: 25px;
}

/* main */
.custom-main {
  display: flex;
  width: 100%;
  padding: 16px 22px;
  align-items: flex-start;
  gap: 30px;
  border: 1px solid #e2e2e2;
  background: #fff;
}

.custom-main-left,
.custom-main-right {
  width: 50%;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.custom-main-left {
  gap: 30px;
  flex: 1 0 0;
  border-right: 1px solid #bfbfbf;
  padding: 16px 30px 16px 22px;
}

.custom-main-right {
  padding: 16px 30px 16px 0px;
}

.custom-left-box {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 24px;
  align-self: stretch;
}

.custom-title {
	display: flex;
    height: 28px;
    align-items: center;
    gap: 6px;
    align-self: stretch;
    justify-content: flex-start;
}

.custom-title span {
  color: #202223;
  font-feature-settings: "clig" off, "liga" off;
  font-size: 18px;
  font-style: normal;
  font-weight: 500;
  line-height: 28px;
}

.custom-control {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  align-self: stretch;
}

.custom-control  span {
	color: var(--Neutral-100, #1C1C1E);
	font-size: 12px;
	font-style: normal;
	font-weight: 500;
	line-height: 22px; /* 183.333% */
}

.custom-control-input {
  width: -webkit-fill-available;
}

.custom-control-input  span {
  color: #1C1C1E;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 22px;
}

.custom-control-input > input {
	margin-top: 6px;
}

.custom-control-2col {
  display: flex;
  align-items: center;
  gap: 16px;
  align-self: stretch;
}

.custom-control-2col > div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  flex: 1 0 0;
}

.custom-control-1col{
  display: flex;
  flex-direction: column;
  width: -webkit-fill-available;
}

.custom-control-number > div,
.custom-control-1col > div,
.custom-control-color > div {
  width: 100%;
  border: 1px solid #939393;
  border-radius: 6px;
  height: 44px;
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: flex-start;
  gap: 10px;
  padding: 8px 12px 10px 8px;
}

.preview{
	margin-top: 30px;
	width: 96%;
}


</style>
