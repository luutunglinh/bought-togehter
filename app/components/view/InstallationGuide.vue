<template>
	<div class="main-comp">
		<div class="installation-title">
			<span>Instalation Guide</span>
			<div class="instalation-btn">
				<button class="m-btn" id="btn-themes">Go to Themes Customization</button>
			</div>
		</div>
		<div class="install-body">
			<div class="install-box">
				<div class="test">
					<span class="title">CONGRATULATION! YOU HAVE CREATED WIDGET SUCCESSFULLY!</span>
					<span class="des">Now please follow these steps below to display it on your product pages</span>
				</div>
				<ol class="text">
					<li>Lorem ipsum is placeholder text commonly used in the graphic, print</li>
                    <li>and publishing industries for previewing layouts and visual mockups.</li>
                    <li>Lorem ipsum is placeholder text commonly used in the graphic, print, and publishing
                        industries for previewing layouts and visual mockups.</li>
				</ol>
			</div>
			<div class="">
				<iframe width="670" height="258" src="https://www.youtube.com/embed/?v=BRMq7-cONsU"
				title="YouTube video player" frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                    allowfullscreen></iframe>
			</div>
		</div>
	</div>
</template>	
<script>
export default {
	name: "installationGuide",
	data() {
		return {}
	},
	methods: {

	}

}
</script>
<style lang="css" scoped>
.installation-title {
	display: flex;
	justify-content: space-between;
    align-items: center;
	width: 100%;
}

.installation-title > span {
	color: #000;
	font-family: Inter;
	font-size: 20px;
	font-style: normal;
	font-weight: 600;
	line-height: 22px; /* 110% */
}

.install-body{
	display: flex;
	width: 100%;
	flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 40px;
    flex-shrink: 0;
    border-radius: 6px;
    border: 1px solid #E2E2E2;
    background: #FFF;
    padding-top: 72px;
    padding-bottom: 72px;
}

.install-box {
	display: flex;
	justify-content: center;
	align-items: center;
	flex-direction: column;
	gap: 20px;
}

.install-box .test {
	display: flex;
    flex-direction: column;
    gap: 30px;
    /* text-align: center; */
    align-items: center;
    justify-content: center;
}

.install-box .title {
	color: #000;
    text-align: center;
    font-size: 20px;
    font-style: normal;
    font-weight: 700;
    line-height: 22px;
}

.install-box .des {
	color: #000;
	font-size: 14px;
	font-style: normal;
	font-weight: 700;
	line-height: 22px;
}

.install-box .text {
	width: 752px;
    color: #000;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 22px; /* 157.143% */
    margin-top: 36px;
}


</style>