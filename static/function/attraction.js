const homeUrl = "http://127.0.0.1:8000/";
const baseUrl = "http://127.0.0.1:8000/api";
const path = window.location.pathname;
const attrPageUrl = baseUrl + path;

// Change guide plan price
const guidePrice = document.querySelector(".attr-price-price");
const radios = document.querySelectorAll("input[type='radio']");

radios.forEach((radio) => {
  radio.addEventListener("change", () => {
    guidePrice.textContent = radio.value;
  });
});

// Fetch Data Response
async function fetchData(attrPageUrl) {
  const response = await fetch(attrPageUrl, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }
  const data = await response.json();
  return data;
}

// Fetch Detail Response
async function displayDetail(attrPageUrl) {
  try {
    createSkeletonInfo();

    const data = await fetchData(attrPageUrl);
    if (!data.data) {
      window.location.assign(homeUrl);
      return;
    }

    document.querySelectorAll(".slides").forEach((slide) => {
      slide.remove();
    });

    createDetailElement(data);
    showSlides(index);
    autoPlay();
  } catch (error) {
    console.error("無法取得景點資料", error);
  }
}

function createDetailElement(data) {
  const slidesContainer = document.querySelector(".slides-container");
  const dotsContainer = document.querySelector(".dots-container");
  const images = data.data.images;

  images.forEach((image, index) => {
    const slides = document.createElement("div");
    slides.classList.add("slides", "fade");
    if (index === 0) {
      slides.style.display = "block";
    }
    const img = document.createElement("img");
    img.src = image;
    slides.appendChild(img);
    slidesContainer.appendChild(slides);

    const dot = document.createElement("span");
    dot.classList.add("dot");
    if (index === 0) {
      dot.classList.add("active");
    }
    dot.onclick = () => currentSlide(index + 1);
    dotsContainer.appendChild(dot);
  });

  const attrTitle = document.querySelector(".attr-title");
  attrTitle.classList.remove("skeleton", "skeleton-bigTitle");
  attrTitle.textContent = data.data.name;

  const attrCategory = document.querySelector(".attr-category");
  attrCategory.classList.remove("skeleton", "skeleton-shortBody");
  attrCategory.textContent = data.data.category;

  const attrMRT = document.querySelector(".attr-mrt");
  attrMRT.classList.remove("skeleton", "skeleton-shortBody");
  attrMRT.textContent = data.data.mrt;

  const desInfo = document.querySelector(".des-info");
  desInfo.classList.remove("skeleton", "skeleton-longText");
  // desInfo.textContent = data.data.description;

  const desLocationInfo = document.querySelector(".des-location-info");
  desLocationInfo.classList.remove("skeleton", "skeleton-shortText");
  desLocationInfo.textContent = data.data.address;

  const desTransInfo = document.querySelector(".des-trans-info");
  desTransInfo.classList.remove("skeleton", "skeleton-shortText");
  desTransInfo.textContent = data.data.transport;

  // slice text and show more button
  const description = data.data.description;
  const maxLength = 300;
  if (description.length > maxLength) {
    const visibleText = description.slice(0, maxLength);
    console.log(visibleText);
    const hiddenText = description.slice(maxLength);
    desInfo.innerHTML = `${visibleText}<span class="hidden-text" style="display: none">${hiddenText}</span><button class="show-more-btn" style="border: none; border-bottom: 1px solid #448899; color: #448899; background-color: transparent; font-size: 16px; font-weight: 400; margin-left: 10px; cursor: pointer; line-height: 14px">瞭解更多</button>`;

    const showMoreBtn = desInfo.querySelector(".show-more-btn");
    const hiddenTextSpan = desInfo.querySelector(".hidden-text");

    showMoreBtn.addEventListener("click", () => {
      if (hiddenTextSpan.style.display === "none") {
        hiddenTextSpan.style.display = "inline";
        showMoreBtn.textContent = "收起資訊";
      } else {
        hiddenTextSpan.style.display = "none";
        showMoreBtn.textContent = "瞭解更多";
      }
    });
  } else {
    desInfo.textContent = description;
  }
}

// Slides
let index = 1;

// prev and next
function plusSlides(n) {
  showSlides((index += n));
}

// dot click
function currentSlide(n) {
  showSlides((index = n));
}

function showSlides(n) {
  let slides = document.querySelectorAll(".slides");
  let dots = document.querySelectorAll(".dot");
  if (n > slides.length) {
    index = 1;
  } else if (n < 1) {
    index = slides.length;
  }

  slides.forEach((slide, i) => {
    slide.style.display = "none";
    if (i === index - 1) {
      slide.style.display = "block";
    }
  });

  dots.forEach((dot, i) => {
    dot.classList.remove("active");
    if (i === index - 1) {
      dot.classList.add("active");
    }
  });
}

function autoPlay() {
  plusSlides(1);
  setTimeout(autoPlay, 4000);
}

// Display skeleton
function createSkeletonInfo() {
  const slides = document.querySelector(".slides");
  slides.classList.add("skeleton");

  plusSlides(1);

  const attrTitle = document.querySelector(".attr-title");
  attrTitle.classList.add("skeleton", "skeleton-bigTitle");

  const attrCategory = document.querySelector(".attr-category");
  attrCategory.classList.add("skeleton", "skeleton-shortBody");

  const attrMRT = document.querySelector(".attr-mrt");
  attrMRT.classList.add("skeleton", "skeleton-shortBody");

  const desInfo = document.querySelector(".des-info");
  desInfo.classList.add("skeleton", "skeleton-longText");

  const desLocationInfo = document.querySelector(".des-location-info");
  desLocationInfo.classList.add("skeleton", "skeleton-shortText");

  const desTransInfo = document.querySelector(".des-trans-info");
  desTransInfo.classList.add("skeleton", "skeleton-shortText");
}

// Call attraction page
displayDetail(attrPageUrl);
