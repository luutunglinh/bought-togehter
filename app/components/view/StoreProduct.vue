<template>
	<Mtoast v-if="isShowToast" :content="content"/>
	<div class="main-comp-item" :class="enable_widget ? '' : 'disabled-row'">
		<div class="main-comp-header">
			<div class="main-comp-title">
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
				<span>{{title_widget}}</span>
			</div>
			<div class="main-comp-search">
				<svg xmlns="http://www.w3.org/2000/svg" height="16" width="16" viewBox="0 0 512 512"><path d="M416 208c0 45.9-14.9 88.3-40 122.7L502.6 457.4c12.5 12.5 12.5 32.8 0 45.3s-32.8 12.5-45.3 0L330.7 376c-34.4 25.2-76.8 40-122.7 40C93.1 416 0 322.9 0 208S93.1 0 208 0S416 93.1 416 208zM208 352a144 144 0 1 0 0-288 144 144 0 1 0 0 288z"/></svg>
				<AutoComplete 
					v-model:value="searchValue"
					:bordered="false"
					placeholder="Search product by name"
					@search="onSearch"
					@focus="onFocus"
					@blur="onBlur"
					size="large"
					class="input"
				/>
				<div class="search-box" v-if="isSearch">
					<div class="search-box-item" v-for="item in dataSearch" :key="item.key" @click="addProduct(item)">
						<div>
                          <img :src="item.url"/>
                          <div>
                              <span class="title"> {{ item.title }} </span>
                              <span class="des">$ {{ item.price }}</span>
                          </div>
                      </div>
					</div>
				</div>
				<div class="selected">
                	<div style="padding-bottom: 3px">{{ selectedRowsCount }} selected</div>
              	</div>
			</div>
		</div>
		<div class="remove-btn" v-if="isDelete" @click="deleteProduct">Remove selected product(s)</div>
		<Table :columns="columns"
			   :data-source="dataTable"
			   :row-selection="rowSelection"
			   :pagination="false"
			   style="width: 100%;" size="small"  
			   >
			<template #headerCell="{title}">
				<template v-if="title">
                  <strong>{{ title }}</strong>
                </template>	
			</template>
			<template #bodyCell="{column, record}">
				<template v-if="column.key === 'url'">
					<img :src="record.url" :alt="record.name" style="'opacity: 0.2; width: 30px; height: 30px' ">
				</template>
				<template v-if="column.key === 'price'">
                	${{ record.price }}
              	</template>
				<template v-if="column.key === 'compare'">
					${{ record.compare }}
				</template>
				<template v-if="column.key === 'quantity'">
					{{ record.quantity }}
				</template>
			</template>
		</Table>
	</div>
	{{ discard }}
</template>
<script>
import _ from 'lodash';
import Mtoast from "./Mtoast.vue"
import { Table, AutoComplete } from 'ant-design-vue';
import axios from 'axios';
export default {
	name: "StoreProduct",
	components: {
		Table,
		AutoComplete,
		Mtoast
	},
	props: {
		enable_widget: Boolean,
		data: {
			type: [String, Number, Object, Array, Boolean],
      		default: null,
		} ,
		title_widget: String,
		save: Number,
    	discard: Number,
		type: String,
	},
	data(){
		return {
			isSearch: false,
			isDelete: false,
			rows: [],
			dataTable: [],
			selectedRowsCount: 0,
			rowSelection: {
				onChange: this.onChange,
				hideSelectAll: this.hideSelectAll
			},
			dataSearch: [],
			data_1: null,
			searchValue:'',
			content: '',
			isShowToast: false,
			columns: [
				{
					key: 'url',
					title: 'Image',
					dataIndex: 'url'
				},
				{
					key: 'title',
					title: 'Product Name',
					dataIndex: 'title'
				},
				{
					key: 'price',
					title: 'Price',
					dataIndex: 'price'
				},
				{
					key: 'compare',
					title: 'Compare at price',
					dataIndex: 'compare'
				},
				{
					title: 'In Stock',
					dataIndex: 'quantity',
					key: 'quantity'
				}
			],
		}
	},
	emits: ['test'],
	mounted() {

	},
	methods: {

		//search
		// onSearch(searchText){
		// 	console.log(searchText);
		// 	this.searchProduct(searchText)
		// },
		onSearch:
			_.debounce(function (searchText) {
			this.isSearch = true
			this.dataSearch = []
			this.searchProduct(searchText)
    			}, 300)
		,
		onFocus(searchText){
			this.searchProduct(searchText)
	
		},
		onBlur(){
			_.delay(() => {
				this.isSearch = false,
				this.dataSearch = [],
				this.searchValue=''
			},50)
		},

		addProduct(item) {
			console.log(item);
			console.log(this.dataTable);
			if(this.dataTable.length < 5){
				const isExist = this.dataTable.some(product => product.key === item.key);
				if (!isExist) {
					this.dataTable =[...this.dataTable, item]
					this.content = "Save Product is successfully added",
						this.isShowToast = true
						_.delay(() => {
							this.isShowToast = false
						}, 3000)
				}
			} else {
				this.content = 'You have reach the product limitation.' 
				+'Please remove any products from the list to continue selecting',
				this.isShowToast = true
				_.delay(() => {
					this.isShowToast = false
				}, 3000)
				
			}
		},
		// function substring
		substringIdProduct(inputString){
			const parts = inputString.split('/');
			const numberValue = parseInt(parts[parts.length - 1], 10);
			return numberValue
		},

		async saveProduct(){
			const url ="/sample-app/save-product"
			await axios.post(url,{
				jsonrpc: "2.0",
				params: {
					'shop': window.app_settings.store,
					'data': this.dataTable,
					'type': this.type
				}
			}).then(res => {
				console.log('saveProduct',res);
			})
		},

		async searchProduct(searchText){
			const url ="/sample-app/search-product"
				await axios.post(url, {
				jsonrpc: "2.0",
				params: {
					'searchText': searchText,
					'shop': window.app_settings.store
				}
				}).then(response => {
					console.log(response.data.result);
					response.data.result.forEach(item => {
						let url = item.node.product.featuredImage ? item.node.product.featuredImage.url : ""
						this.dataSearch.push({
							key: this.substringIdProduct(item.node.id), 
							title: item.node.product.title,
							url: url,
							price: item.node.price,
							compare: item.node.compareAtPrice,
							quantity: item.node.inventoryQuantity
						})
					})
					console.log(this.dataSearch);
				}).catch((error) => {
        			console.log(error)
      			})
				
		},

		onChange(selectedRowKeys){
			console.log('onChange', selectedRowKeys);
			this.selectedRowsCount = selectedRowKeys.length
			if(selectedRowKeys.length > 0 ){
				this.rows = selectedRowKeys
				console.log(this.rows);
				this.isDelete = true
			} else {
				this.isDelete = false
			}
		},
		deleteProduct() {
			console.log(this.rows);
			this.dataTable = this.dataTable.filter(item => !this.rows.includes(item.key))
			this.rows = []
			this.isDelete = false
			this.selectedRowsCount = 0
		}
	},
	watch: {
		data() {
			this.dataTable = this.data
    	},
		discard(){
      		this.dataTable = this.data
		},
		save() {
			this.saveProduct()
		}
	
    },
}
</script>
<style lang="css" scoped>

.main-comp-header {
  display: flex;
  height: 80px;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  align-self: stretch;

}

.main-comp-title {
	display: flex;
	align-items: center;
	gap: 10px;
}

.main-comp-search{
	display: flex;
	position: relative;
	width: 100%;
	align-items: center;
}


.main-comp-search > svg {
  transform: translate(14px, 1px);
  position: absolute;
}

.main-comp-search .input {
  display: flex;
  align-items: center;
  padding-left: 32px;
  border: 1px solid #E6E6E6;
  border-radius: 6px 0 0 6px;
  width: 100%;
}

.main-comp-search span {
  width: 100%;
  border-radius: 5px;
  margin-left: 20px;
  margin-top: 4px;
  margin-right: 23px;
}

.search-box {
  position: absolute;
  left: 0;
  top: 44px;
  width: calc(100% - 120px);
  display: flex;
  padding: 8px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 4px;
  border-radius: 0 0 6px 6px;
  border: 1px solid #D1D1D1;
  background-color: #fff;
  z-index: 10;
}

.search-box-item {
  display: flex;
  padding: 12px 16px;
  align-items: center;
  gap: 16px;
  align-self: stretch;
  border-radius: 8px;
  background: var(--background-color);
}

.search-box-item > div {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  flex: 1 0 0;
}

.search-box-item:hover {
  cursor: pointer;
  background: #E9F6FF;
}

.search-box-item > div > div {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  flex: 1 0 0;
}

.search-box-item > div >img {
  width: 44px;
  height: 44px;
  border-radius: 4px;
}

.search-box-item > .des{
  color: #636366;
  font-size: 12px;
  font-weight: 400;
  line-height: 18px;
}

.search-box-item .title {
	color: var(--Neutral-100, #1C1C1E);
    font-size: 14px;
    font-style: normal;
    font-weight: 500;
    line-height: 20px;
}

.main-comp-search .selected {
	display: flex;
	height: 42px;
	padding: 7px 15px;
	justify-content: center;
	align-items: center;
	gap: 10px;
	border-radius: 0px 6px 6px 0px;
	border-top: 1.21px solid #E6E6E6;
	border-right: 1.21px solid #E6E6E6;
	border-bottom: 1.21px solid #E6E6E6;
	background: #FFF;
	min-width: 120px;
}

.remove-btn {
  color: #F00;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  margin-bottom: 8px;
}

.remove-btn:hover {
  cursor: pointer;
  text-decoration: underline;
}

.disabled-row {
  pointer-events: none;
  color: #dcdcdc;
}
</style>