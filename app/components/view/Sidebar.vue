<template>
	<div id="side-bar">
		<div class="side-title">
			<div class="image">
				<svg
				width="46"
				height="46"
				viewBox="0 0 46 46"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
				>
				<circle cx="23" cy="23" r="23" fill="black" />
				</svg>
			</div>
			<span>NestScale</span>
		</div>
		<div class="side-menu">
			<a class="item"
				@click="redirectURL('/dashboard/store')"
				:class="{active : addProductActive}"
			>
				<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          		<path
					d="M5.52 2.64L3.96 4.72C3.65102 5.13198 3.49652 5.33797 3.50011 5.51039C3.50323 5.66044 3.57358 5.80115 3.69175 5.89368C3.82754 6 4.08503 6 4.6 6H19.4C19.915 6 20.1725 6 20.3083 5.89368C20.4264 5.80115 20.4968 5.66044 20.4999 5.51039C20.5035 5.33797 20.349 5.13198 20.04 4.72L18.48 2.64M5.52 2.64C5.696 2.40533 5.784 2.288 5.89552 2.20338C5.9943 2.12842 6.10616 2.0725 6.22539 2.03845C6.36 2 6.50667 2 6.8 2H17.2C17.4933 2 17.64 2 17.7746 2.03845C17.8938 2.0725 18.0057 2.12842 18.1045 2.20338C18.216 2.288 18.304 2.40533 18.48 2.64M5.52 2.64L3.64 5.14666C3.40254 5.46328 3.28381 5.62159 3.1995 5.79592C3.12469 5.95062 3.07012 6.11431 3.03715 6.28296C3 6.47301 3 6.6709 3 7.06666L3 18.8C3 19.9201 3 20.4802 3.21799 20.908C3.40973 21.2843 3.71569 21.5903 4.09202 21.782C4.51984 22 5.07989 22 6.2 22L17.8 22C18.9201 22 19.4802 22 19.908 21.782C20.2843 21.5903 20.5903 21.2843 20.782 20.908C21 20.4802 21 19.9201 21 18.8V7.06667C21 6.6709 21 6.47301 20.9628 6.28296C20.9299 6.11431 20.8753 5.95062 20.8005 5.79592C20.7162 5.62159 20.5975 5.46328 20.36 5.14667L18.48 2.64M16 10C16 11.0609 15.5786 12.0783 14.8284 12.8284C14.0783 13.5786 13.0609 14 12 14C10.9391 14 9.92172 13.5786 9.17157 12.8284C8.42143 12.0783 8 11.0609 8 10"
					stroke="#939393" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        		</svg>
				<span>Add Product</span>
			</a>
			<a class="item"
				@click="redirectURL('/dashboard/customization')"
				:class = "{active: customizationActive}"
			>
				<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          		<path
              d="M13 14L9.99997 11M15.0103 3.5V2M18.9497 5.06066L20.0103 4M18.9497 13L20.0103 14.0607M11.0103 5.06066L9.94966 4M20.5103 9H22.0103M6.13134 20.8686L15.3686 11.6314C15.7646 11.2354 15.9626 11.0373 16.0368 10.809C16.1021 10.6082 16.1021 10.3918 16.0368 10.191C15.9626 9.96265 15.7646 9.76465 15.3686 9.36863L14.6313 8.63137C14.2353 8.23535 14.0373 8.03735 13.809 7.96316C13.6081 7.8979 13.3918 7.8979 13.191 7.96316C12.9626 8.03735 12.7646 8.23535 12.3686 8.63137L3.13134 17.8686C2.73532 18.2646 2.53732 18.4627 2.46313 18.691C2.39787 18.8918 2.39787 19.1082 2.46313 19.309C2.53732 19.5373 2.73533 19.7354 3.13134 20.1314L3.8686 20.8686C4.26462 21.2646 4.46263 21.4627 4.69095 21.5368C4.8918 21.6021 5.10814 21.6021 5.30899 21.5368C5.53732 21.4627 5.73533 21.2646 6.13134 20.8686Z"
              stroke="#939393" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        		</svg>
        		<span>Customization</span>
			</a>
			<a class="item"
				@click="redirectURL('/dashboard/installationGuide')"
				:class="{active:installationGuideActive}"
			>
				<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
          		<path
              d="M12 2V3M3 12H2M5.5 5.5L4.8999 4.8999M18.5 5.5L19.1002 4.8999M22 12H21M10 13.5H14M12 13.5V18.5M15.5 16.874C17.0141 15.7848 18 14.0075 18 12C18 8.68629 15.3137 6 12 6C8.68629 6 6 8.68629 6 12C6 14.0075 6.98593 15.7848 8.5 16.874V18.8C8.5 19.9201 8.5 20.4802 8.71799 20.908C8.90973 21.2843 9.21569 21.5903 9.59202 21.782C10.0198 22 10.5799 22 11.7 22H12.3C13.4201 22 13.9802 22 14.408 21.782C14.7843 21.5903 15.0903 21.2843 15.282 20.908C15.5 20.4802 15.5 19.9201 15.5 18.8V16.874Z"
              stroke="#939393" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        		</svg>
				<span>Installation Guide</span>
			</a>
		</div>
		{{ comp }}
	</div>
</template>
<script>
export default {
	name: "Sidebar",
	props: ['comp'],
	mounted() {
		console.log('props_comp',this.comp);
	},
	created(){
    },		
	data() {
		return {
			addProductActive: false,
			customizationActive: false,
			installationGuideActive: false,
		}
	},
	methods: {
		redirectURL(url){
			history.pushState({},'',url)
		}
	},
	watch: {
		comp() {
			if(this.comp === 'store'){
				this.addProductActive = true
				this.customizationActive = false
				this.installationGuideActive = false
			}
			else if (this.comp === 'customization'){
				this.addProductActive = false
				this.customizationActive = true
				this.installationGuideActive = false
			} else if (this.comp === 'installationGuide') {
				this.addProductActive = false
				this.customizationActive = false
				this.installationGuideActive = true
			}
			else {
				this.addProductActive = true
				this.customizationActive = false
				this.installationGuideActive = false
			}
	}
}

}
</script>
<style lang="css" scoped>
#side-bar{
	display: flex;
	position: fixed;
	flex-direction: column;
	align-items: flex-start;
	flex-shrink: 0;
	background-color: #FFFFFF;
	gap: 32px;
	width: 276px;
	height: 1135px;
	padding: 24px 20px 0 20px;
	z-index: 15;
}
.side-title {
	display: flex;
	align-items: center;
	gap: 12px
}

.side-title > .image {
	height: 46px;
	width: 46px;
	border-radius: 50%;
	background: black;
		
}

.side-title > span {
	color: #17181A;
	font-size: 27px;
	font-style: normal;
	font-weight: 600;
	align-items: flex-start;
	font-family: Kanit, sans-serif;
}

.side-menu {
	display: flex;
	width: 238px;
	flex-direction: column;
	align-items: flex-start;
	gap: 8px;
}

.side-menu .item {
	display: flex;
	padding: 12px;
	align-items: center;
	gap: 12px;
	align-self: stretch;
	user-select: none;
}

.side-menu .item:hover {
	border-radius: 12px;
	background: #ECECEC;
	cursor: pointer;
}

.item.active {
  border-radius: 12px;
  background: #ECECEC;
}

.side-menu .item span {
  color: #939393;
  font-size: 14px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
}


</style>