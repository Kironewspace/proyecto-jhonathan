function toggleMenu() {
  const menu = document.getElementById("menu");
  const hamburger = document.querySelector(".hamburger");
  menu.classList.toggle("active");
  hamburger.classList.toggle("active");
  const isActive = menu.classList.contains("active");
  hamburger.setAttribute("aria-expanded", isActive);
}


const slideTrack = document.getElementById('slideTrack');
const slides = document.querySelectorAll('.slide');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let currentIndex = 0;

function updateSlidePosition() {
  const offset = currentIndex * -100; 
  slideTrack.style.transform = `translateX(${offset}%)`;
}

function nextSlide() {
  currentIndex = (currentIndex + 1) % slides.length;
  updateSlidePosition();
}

function prevSlide() {
  currentIndex = (currentIndex - 1 + slides.length) % slides.length;
  updateSlidePosition();
}


setInterval(nextSlide, 5000);


nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);

