{
	class Details {
		constructor() {
			this.DOM = {};

			const detailsTmpl = `
			<div class="details__bg details__bg--down">
				<button class="details__close"><i class="fas fa-2x fa-times icon--cross tm-fa-close"></i></button>
				<div class="details__description"></div>
			</div>
			`;

			this.DOM.details = document.createElement('div');
			this.DOM.details.className = 'details';
			this.DOM.details.innerHTML = detailsTmpl;
			// DOM.content.appendChild(this.DOM.details);
			document.getElementById('tm-wrap').appendChild(this.DOM.details);
			this.init();
		}
		init() {
			this.DOM.bgDown = this.DOM.details.querySelector('.details__bg--down');
			this.DOM.description = this.DOM.details.querySelector('.details__description');
			this.DOM.close = this.DOM.details.querySelector('.details__close');

			this.initEvents();
		}
		initEvents() {
			// close page when outside of page is clicked.
			document.body.addEventListener('click', () => this.close());
			// prevent close page when inside of page is clicked.
			this.DOM.bgDown.addEventListener('click', function(event) {
				event.stopPropagation();
			});
			// close page when cross button is clicked.
			this.DOM.close.addEventListener('click', () => this.close());
		}
		fill(info) {
			// fill current page info
			this.DOM.description.innerHTML = info.description;
		}
		getProductDetailsRect(){
			var p = 0;
			var d = 0;

			try {
				p = this.DOM.productBg.getBoundingClientRect();
				d = this.DOM.bgDown.getBoundingClientRect();
			}
			catch(e){}

			return {
				productBgRect: p,
				detailsBgRect: d
			};
		}
		open(data) {
			if(this.isAnimating) return false;
			this.isAnimating = true;

			this.DOM.details.style.display = 'block';

			this.DOM.details.classList.add('details--open');

			this.DOM.productBg = data.productBg;

			this.DOM.productBg.style.opacity = 0;

			const rect = this.getProductDetailsRect();

			this.DOM.bgDown.style.transform = `translateX(${rect.productBgRect.left-rect.detailsBgRect.left}px) translateY(${rect.productBgRect.top-rect.detailsBgRect.top}px) scaleX(${rect.productBgRect.width/rect.detailsBgRect.width}) scaleY(${rect.productBgRect.height/rect.detailsBgRect.height})`;
			this.DOM.bgDown.style.opacity = 1;

			// animate background
			anime({
				targets: [this.DOM.bgDown],
				duration: (target, index) => index ? 800 : 250,
				easing: (target, index) => index ? 'easeOutElastic' : 'easeOutSine',
				elasticity: 250,
				translateX: 0,
				translateY: 0,
				scaleX: 1,
				scaleY: 1,
				complete: () => this.isAnimating = false
			});

			// animate content
			anime({
				targets: [this.DOM.description],
				duration: 1000,
				easing: 'easeOutExpo',
				translateY: ['100%',0],
				opacity: 1
			});

			// animate close button
			anime({
				targets: this.DOM.close,
				duration: 250,
				easing: 'easeOutSine',
				translateY: ['100%',0],
				opacity: 1
			});

			this.setCarousel();

			window.addEventListener("resize", this.setCarousel);
		}
		close() {
			if(this.isAnimating) return false;
			this.isAnimating = true;

			this.DOM.details.classList.remove('details--open');

			anime({
				targets: this.DOM.close,
				duration: 250,
				easing: 'easeOutSine',
				translateY: '100%',
				opacity: 0
			});

			anime({
				targets: [this.DOM.description],
				duration: 20,
				easing: 'linear',
				opacity: 0
			});

			const rect = this.getProductDetailsRect();
			anime({
				targets: [this.DOM.bgDown],
				duration: 250,
				easing: 'easeOutSine',
				translateX: (target, index) => {
					return index ? rect.productImgRect.left-rect.detailsImgRect.left : rect.productBgRect.left-rect.detailsBgRect.left;
				},
				translateY: (target, index) => {
					return index ? rect.productImgRect.top-rect.detailsImgRect.top : rect.productBgRect.top-rect.detailsBgRect.top;
				},
				scaleX: (target, index) => {
					return index ? rect.productImgRect.width/rect.detailsImgRect.width : rect.productBgRect.width/rect.detailsBgRect.width;
				},
				scaleY: (target, index) => {
					return index ? rect.productImgRect.height/rect.detailsImgRect.height : rect.productBgRect.height/rect.detailsBgRect.height;
				},
				complete: () => {
					this.DOM.bgDown.style.opacity = 0;
					this.DOM.bgDown.style.transform = 'none';
					this.DOM.productBg.style.opacity = 1;
					this.DOM.details.style.display = 'none';
					this.isAnimating = false;
				}
			});
		}
		// Slick Carousel
		setCarousel() {

			var slider = $('.details .tm-img-slider');

			if(slider.length) { // check if slider exist

				if (slider.hasClass('slick-initialized')) {
					slider.slick('destroy');
				}

				if($(window).width() > 767){
					// Slick carousel
					slider.slick({
						dots: true,
						infinite: true,
						slidesToShow: 4,
						slidesToScroll: 3
					});
				}
				else {
					slider.slick({
						dots: true,
						infinite: true,
						slidesToShow: 2,
						slidesToScroll: 1
					});
				}
			}
		}
	}; // class Details

	class Item {
		constructor(el) {
			this.DOM = {};
			this.DOM.el = el;
			this.DOM.product = this.DOM.el.querySelector('.product');
			this.DOM.productBg = this.DOM.product.querySelector('.product__bg');

			this.info = {
				description: this.DOM.product.querySelector('.product__description').innerHTML
			};

			this.initEvents();
		}
		initEvents() {
			this.DOM.product.addEventListener('click', () => this.open());
		}
		open() {
			DOM.details.fill(this.info);
			DOM.details.open({
				productBg: this.DOM.productBg
			});
		}
	}; // class Item

	const DOM = {};
	DOM.grid = document.querySelector('.grid');
	DOM.content = DOM.grid.parentNode;
	DOM.gridItems = Array.from(DOM.grid.querySelectorAll('.grid__item'));
	let items = [];
	DOM.gridItems.forEach(item => items.push(new Item(item)));

	DOM.details = new Details();
};


