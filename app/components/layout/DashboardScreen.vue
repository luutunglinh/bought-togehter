<template>
    <div class="dashboard">
		<Sidebar :comp="activeComp"></Sidebar>
		<Navbar :user_image="user_image"></Navbar>
		<div class="main">
			<component :is="activeComp"></component>
		</div>
    </div>
</template>
<script>
import InstallationGuide from '../view/InstallationGuide.vue';
import Store from '../view/Store.vue';
import Navbar from '../view/Navbar.vue';
import Sidebar from '../view/Sidebar.vue';
import Settings from '../view/Settings.vue';
import Customization from '../view/Customization.vue';
export default {
    name:"Dashboard",
	components: {
    Sidebar,
    Navbar,
	Settings,
	Store,
	InstallationGuide,
	Customization
},	
    data() {
        return {
			currentComponent: window.app_settings.name,
			user_name: window.app_settings.user_name,
      		user_image: window.app_settings.user_image,
			pathName: window.location.pathname,
			stores: window.app_settings.stores,
			activeComp: '',
		}
    },
    methods: {
		setUrl(){			
			switch(	this.pathName = window.location.pathname){
				case "/dashboard/store":
					this.activeComp = 'store'
					break
				case "/dashboard/customization":
					this.activeComp = 'customization'
					break
				case "/dashboard/installationGuide":
					this.activeComp= 'installationGuide'
					break
				default: 
					if(this.pathName.includes('/dashboard/store/')){
						const store_name = this.pathName.split('/dashboard/store/')[1]
						const exist_name = this.stores.map(item => item.name).includes(store_name)
						if(exist_name){
							window.app_settings.store = store_name
							this.activeComp = 'Settings'
						}

					}
					
			}
		}
	},
	created() {
		this.setUrl()
		window.addEventListener('click', () => {
      	this.setUrl()
    });
	}
}
</script>
<style lang="css" scoped>
.dashboard {
	width: 100%;
	min-height: 1003px;
	display: flex;
	flex-direction: row;
	background-color: #f4f4f4;
}

.dashboard .main {
  width: 100%;
  margin: 103px 25px 34px 301px;
}

</style>