<template>
		<div class="custom-box">
			<div class="custom-box-right">
				<div>
					<span class="rb-main-title" :style="{ color: title_color, fontSize: title_font_size + 'px' }">
						{{ widget_title }}
					</span>
				</div>
				<div>
					<span class="rb-main-des" :style="{ color: description_color, fontSize: description_font_size + 'px'}">
						{{ widget_description }}
					</span>
				</div>


			
			</div>

			<div class="custom-box-cart">
					<div class="custom-box-image">
						<div v-for="item in products" :key="item.key" class="rb-cart-image">
							<img :src="item.url"
                        		style="border: 1px solid #E2E2E2; border-radius: 5px; width: 65px; height: 65px">
						</div>
					</div>
						<div class="custom-box-buy">
							<div class="custom-box-price">
								<span>Total:</span>
								<span style="color: #FF0000">${{ totalPrice }}</span>
								<span style="color: #848484; text-decoration: line-through">${{ totalPriceCompare }}</span>
							</div>
							<div class="custom-box-btn">
								<button :style="{ background: background_color, borderColor: border_color, color: text_color }" class="btn-buynow" @click="addToCart">{{btn_text}}</button>
							</div>
						</div>
				</div>


			<div class="custom-box-products">
				<div class="custom-box-product">
					<div v-for="item in products" :key="item.key" class="test">
						<div class="test0">
							<Checkbox v-model:checked="item.isActive"></Checkbox>
							{{ item.name }}
						</div>
						<div class="test1">
								<span style="color: #FF0000">${{ item.price }}</span>
						</div>
					</div>
				</div>
			</div>
		</div>
</template>
<script>
import { Checkbox } from "ant-design-vue";
export default {
	name: 'Preview',
	components: {
		Checkbox,
	},
	props: [
		'title_color','title_font_size','widget_title','description_color',
		'description_font_size','widget_description','background_color',
		'border_color','text_color','btn_text','data'
	],	
	emits: ['addToCart'],
	data(){
		return {

		}
	},
	methods: {
		addToCart: function(){
			this.$emit('addToCart',{})
		},
	},
	computed: {
		products(){
			if(this.data){
				return this.data.filter(item => item.isActive)
			} else {
				return []
			}
			
		},
		totalPrice(){
			const result = this.products.reduce((total, product) =>{
				return total + (product.price ? parseInt(product.price) : 0)
			},0)
			return result
		},
		totalPriceCompare(){
			const result = this.products.reduce((total, product) =>{
				return total + (product.compare !== null ? parseInt(product.compare) : 0)
			},0)
			return result*10
		}
	}
}
</script>
<style lang="css" scoped>
.custom-box{
  display: flex;
  padding-left: 0px;
  padding-right: 20px;
  padding-top: 16px;
  padding-bottom: 16px;
  flex-direction: column;
  align-items: flex-start;
  gap: 16px;
  border-radius: 6px;
  border: 1px solid #E2E2E2;
  background: #FFF;
  width: 95%;
  max-width: 120%;
}

.custom-box-right {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 20px;
	width: 100%;
}

.custom-box-cart{
	display: flex;
  	width: 90%;
	margin-left: 30px;
}

.custom-box-image{
	display: flex;
	flex-grow: 1;
	flex-wrap: wrap;
	gap: 40px;
}


.rb-cart-image {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}


.custom-box-buy{
	display: flex;
	flex-direction: column;
	gap: 10px;
	align-items: flex-start;
} 

.custom-box-price{
	display: flex;
	justify-content: space-between;
	align-items: center;
	gap: 16px;
}

.custom-box-price > span {
	color: #000;
	text-align: center;
	font-size: 16px;
	font-style: normal;
	font-weight: 600;
	line-height: 22px; 
}

.custom-box-btn > button{
  display: flex;
  width: 157px;
  padding: 4px 12px;
  justify-content: center;
  align-items: center;
  gap: 10px;
  border-radius: 6px;
  border: 1px solid #1890FF;
  background: #1890FF;
  color: white;
}

.custom-box-btn > button:hover{
	cursor: pointer;
}

.custom-box-products {
	width: 100%;
	margin-left: 30px;
}

.test0 {
	width: 70%;
}

.custom-box-product{
	display: flex;
	padding: 0px 12px;
	flex-direction: column;
	justify-content: center;
	align-items: flex-start;
	gap: 6px;
	width: 100%;
}

.test {
	display: flex;
    align-items: center;
    width: 70%;
	justify-content: space-between;
}

.test > span {
	color: #000;
	text-align: center;
	font-size: 16px;
	font-style: normal;
	font-weight: 600;
	line-height: 22px; 
}

.test1 {
	width: 0%;
}

/* @media only screen and (min-width: 500px) and (max-width: 2000px) {
	.custom-box{
		display: flex;
		padding: 16px 20px;
		flex-direction: column;
		align-items: flex-start;
		gap: 16px;
		border-radius: 6px;
		border: 1px solid #E2E2E2;
		background: #FFF;
		width: 110%;
		max-width: 120%;
		}
} */



</style>