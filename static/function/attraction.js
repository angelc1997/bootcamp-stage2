const baseUrl = "http://127.0.0.1:8000/api";
const path = window.location.pathname;
const attrPageUrl = baseUrl + path;

// attraction

async function fetchDetail(attrPageUrl) {
  try {
    const response = await fetch(attrPageUrl);
    console.log(response);
    const data = await response.json();
    console.log(data);
    if (!data.data) {
      window.location.assign("http://127.0.0.1:8000/");
      return;
    }

    const slides = document.querySelector(".slides");
    const img = document.createElement("img");
    img.src = data.data.images[0];
    slides.appendChild(img);

    const attrTitle = document.querySelector(".attr-title");
    attrTitle.textContent = data.data.name;

    const attrCategory = document.querySelector(".attr-category");
    attrCategory.textContent = data.data.category;

    const attrMRT = document.querySelector(".attr-mrt");
    attrMRT.textContent = data.data.mrt;

    const desInfo = document.querySelector(".des-info");
    desInfo.textContent = data.data.description;

    const desLocationInfo = document.querySelector(".des-location-info");
    desLocationInfo.textContent = data.data.address;

    const desTransInfo = document.querySelector(".des-trans-info");
    desTransInfo.textContent = data.data.transport;
  } catch (error) {
    console.error(`無法取得景點資料，請檢查網址是否正確，或連線狀態是否正常。`);
  }
}

// Change guide plan price
const guidePrice = document.querySelector(".attr-price-price");
const radios = document.querySelectorAll("input[type='radio']");

radios.forEach((radio) => {
  radio.addEventListener("change", () => {
    guidePrice.textContent = radio.value;
  });
});

//  Call attraction page
fetchDetail(attrPageUrl);
