<template>
	<div class="bt-app" >
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
		@addToCart = "addToCart"
		/>
</div>

</template>
<script>
import axios from 'axios';
import Preview from './components/view/Preview.vue';
export default {
    name: "ShopifyFrontend",
	components: {
		Preview
	},
	data(){
		return{
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
		]
		}
	},
	
	async created(){

		const url = '/apps/bt/sample-app/get_widget_data'
		await axios.post(url,{
			jsonrpc:  "2.0",
			params: {
				'shop': window.Shopify.shop.split(".myshopify.com")[0],
				'shop_id': 6,
				'type': 'recommendation'
			}
		})
		.then(res => {
			console.log('getDataCustomization',res.data.result);
			this.data = res.data.result.map(item=> ({...item, isActive: true}))

	})
	},

	async mounted(){
		const url= "/apps/bt/sample-app/get_customization"
		await axios.post(url, {
			jsonrpc: "2.0",
			params: {
				'user_id': 2,
			}
		}).then(response => {
			let data = JSON.parse(response.data.result)
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


		const url_Active = window.location.origin + window.location.pathname + ".js"
		await axios.get(url_Active).then(res => {
			console.log("res",res.data);
			let test = this.data.find(item => {
				return item.key == res.data.variants[0].id
			})
			console.log('exist:', test);
			if (!test) {
				this.data[0] = {
					key: res.data.variants[0].id,
					name: res.data.variants[0].name,
					url: res.data.featured_image || res.data.images[0],
					price: res.data.price,
					compare: res.data.compare_at_price,
					isActive: true,
				}
			}
		})
	},
	methods: {
		async addToCart(){
			const formData ={
				items: this.data.map(item => ({
					id: item.key,
          			quantity: 1,
				}))
			}
			const urlAddToCart = window.location.origin +"/cart/add.js"
			axios.post(urlAddToCart,formData, {
				headers: {
					'Content-Type': 'application/json'
				}
			}).then(response => {
				console.log('Response from Shopify:', response.data);
			})

		}
	}
}
</script>

<style scoped lang="css">
.bt-app{
	width: 45%;
    margin: 20px auto
}

@media (min-width: 1600px) {
	.bt-app{
		max-width: 57%;
    	margin: 20px auto
		}
}


</style>