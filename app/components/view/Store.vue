<template>
	<div class="main-comp">
		<span class="title">WELCOME {{ user_name }}</span>
		<div class="main-comp-body">
			<div class="main-comp-item">
				<div class="main-btn" v-if="isShow">
					<Button @click="enableSelected">Enable selected store(s)</Button>
          			<Button @click="disableSelected">Disable selected store(s)</Button>
				</div>
				<Table :columns="columns" :data-source="data" :row-selection="rowSelection" :pagination="false" style="width: 100%" size="small" >
					<template #bodyCell ="{column, record}">
						<template v-if="column.key === 'name'">
              				<a @click="redirectStore(record.key)">{{ record.name }}</a>
            			</template>
						<template v-else-if="column.key === 'status'">
							<Switch @click="changeStatus(record.key,record.status)" v-model:checked="record.status" checked-children="ON" un-checked-children="OFF"></Switch>
						</template>
					</template>
				</Table>
			</div>
		</div>
	</div>
</template>
<script>
import { Table, Button, Switch } from 'ant-design-vue'
import axios from "axios";
export default {
	name: "Store",
	components: {Button,Table,Switch},
	created () {
		//this.changeStore_Status()
	},
	data(){
		return {
			user_name: window.app_settings.user_name,
			isShow: false,
			rows: [],
			rowSelection: {
				onSelect: this.onSelect,
				onSelectAll: this.onSelectAll,
				selectedRowKeys: this.selectedRowKeys
			},
			columns: [
				{
					title: "Store",
					dataIndex: 'name',
					key: 'name',
					width: '80%'
				},
				{
					title: "Products Included",
					dataIndex: 'product_included',
					key:'product_included',
					width: '150px'
					
				},
				{
					title: "Status",
					dataIndex: 'status',
          			key: 'status',
					width: '124px'
				}
			],
			data: window.app_settings.stores
		}
	},
	methods: {
		async changeStatus(store, status){
			try {
				const url = '/sample-app/store-status'
				await axios.post(url,{
					jsonrpc: "2.0",
					params: {
						'store': store,
						'status': status
					}
				}).then(response => {
					console.log(response.data);
				})
			}
			catch(error) {
				console.error('Error:', error);
			}
		},
		onSelect(record, selected, selectedRows){
			if(selectedRows.length){
				this.isShow = true;
				this.rows = selectedRows.map(item => item.key)
			} else {
				this.isShow = false;
				this.rows = []
			}
		},
		onSelectAll(selected, selectedRows){
			if(selected){
				this.isShow = true,
				this.rows = selectedRows.map(item => item.key)
			}
			else {
				this.isShow = false;
				this.rows = []
			}
		},
		enableSelected() {
			this.rows.map(item => {
				this.changeStore_Status(item,true)
			})	
			this.data.map(item =>{
				if (this.rows.includes(item.key)) {
					item.status = true;
				}
			})
		},
		disableSelected(){
			this.rows.map(item => {
				this.changeStore_Status(item,false)
			})	
			this.data.map(item =>{
				if (this.rows.includes(item.key)) {
					item.status = false;
				}
			})
		},
		redirectStore(store){
			let url = '/dashboard/store/' + store
			history.pushState({},'',url)
		},

	},
}
</script>
<style lang="css" scoped>
.main-btn {
	display: flex;
	align-items: center;
	gap: 30px;
}
.main-btn Button {
	border-radius: 6px;
    color: #1890FF;
}

</style>