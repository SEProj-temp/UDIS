const btnPopup = document.querySelector('.btnLogin-popup');

const swiper = new Swiper('.swiper', {
	pagination: {
		el: '.swiper-pagination',
	},

	// Navigation arrows
	navigation: {
		nextEl: '.swiper-button-next',
		prevEl: '.swiper-button-prev',
	},
});

window.addEventListener("scroll", () => {
	document.querySelector('nav').classList.toggle('scroll', window.scrollY > 0)
})

btnPopup.addEventListener("click", () => {
	wrapper.classList.add('active-popup');
})
