<template>
	<div class="main-comp">
		<div class="settings-title">
			<div class="header_name_store">
				<span>Manual Recommendation</span>
			</div>
			<div class="header_btn_store">
				<button @click="discardProduct" class="btn btn-cancel">Discard</button>
				<button @click="saveProduct" class="btn btn-next">Save</button>
			</div>
		</div>
		<div class="main-comp-body">
			<div class="settings-switch">
				<span>Enable Widget</span>
				<Switch 
					@click="changeStatus" v-model:checked="isEnable" 
					checked-children="ON" 
					un-checked-children="OFF"
				/>
			</div>
			<StoreProduct
				:discard = "discard"
				:save = "save"
				:enable_widget="isEnable"
				:data="dataRecommendTable"
				title_widget="Choose recommendation product(s)"
				type="recommendation"
			/>
			<StoreProduct
				:discard = "discard"
				:save = "save"
				:enable_widget="isEnable"
				:data="dataExcludedTable"
				title_widget="Choose excluded product(s)"
				type="excluded"
			/>
		</div>
	</div>
</template>
<script>
import axios from "axios";
import StoreProduct from './StoreProduct.vue';
import { Switch } from 'ant-design-vue'
export default {
		name: "Settings",
		components: {
			Switch,
			StoreProduct
		},
		created() {
			this.getDataStore()
		},
		data(){
			return {
				dataRecommendTable: [],
				dataExcludedTable: [],
				temporary_data: null,
				isEnable: false,
				discard: 0,
				save: 0
			}
		},
		methods: {
			async getDataStore(){
				try {
					const url = '/sample-app/get-data-store'
					axios.post(url, {
					jsonrpc: "2.0",
					params: {
						'name': window.app_settings.store,
					},
					}).then(response => {
						this.isEnable = response.data.result.store_status
						this.dataRecommendTable = response.data.result.dataRecommendTable
						this.dataExcludedTable = response.data.result.dataExcludedTable
					})
				}
				catch (e) {
					console.log(e);
				}
			},
			async changeStatus(){
				const url = '/sample-app/store-status'
				await axios.post(url,{
				jsonrpc: "2.0",
				params: {
					'store': window.app_settings.store,
          			'status': this.isEnable,
				}
				}).then(response => {
					console.log('test', response.data);
				}).catch(error => {
					console.error('Error:', error);
				});
			},
			saveProduct() {
				this.save = this.save + 1
			},
			discardProduct(){
				this.discard = this.discard + 1
			}
		},
		
	}
</script>
<style lang="css" scoped>
.main-comp {
  position: relative;
  margin-top: 20px;
}

.main-comp .settings-title {
	display: flex;
    width: 100%;
    justify-content: space-between;
    align-items: center;
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

.settings-switch{
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.settings-switch span {
	color: #000;
    font-size: 18px;
    font-style: normal;
    font-weight: 600;
    line-height: 22px;
}

.btn-next {
  gap: 4px;
  width: 62px;
  height: 32px;
  color: white;
  font-weight: 700;
  border: #1D1E21;
  background: #1D1E21;

}

.btn-cancel {
  font-weight: 500;
  border: #E2E2E2;
  flex: none;
  order: 1;
  flex-grow: 0;
  width: 71px;
  height: 32px;
  background: #fff;
  margin-right: 25px;
}


</style>