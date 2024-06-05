const baseUrl = "http://127.0.0.1:8000/api";

// Fetch Data Response
async function fetchData(url) {
  const response = await fetch(url, {
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

//  Fetch Tags
async function fetchTags() {
  try {
    let mrtAPI = `${baseUrl}/mrts`;
    let data = await fetchData(mrtAPI);
    let mrtdata = data.data;

    mrtdata.forEach((mrt) => {
      const tagList = document.querySelector(".tag-list");
      const tag = document.createElement("div");
      tag.setAttribute("class", "tag");
      tag.textContent = mrt;
      tagList.appendChild(tag);
    });

    const clickTag = document.querySelectorAll(".tag");
    const searchInput = document.getElementById("search-input");
    clickTag.forEach((tag) => {
      tag.addEventListener("click", () => {
        searchInput.classList.add("searching");
        document.getElementById("search-input").value = tag.textContent;
      });
    });
  } catch (error) {
    console.error("無法取得捷運標籤：", error);
  }
}

// Drag Tags
const tagList = document.querySelector(".tag-list");
const icons = document.querySelectorAll(".tag-icon");

icons.forEach((icon) => {
  icon.addEventListener("click", () => {
    tagList.scrollLeft += icon.id === "next" ? 600 : -600;
  });
});

let pageNumbers = [];
let keywords = [];

// Fetch Attractions
async function fetchFirstPage() {
  try {
    let attrAPI = `${baseUrl}/attractions?page=0`;
    let data = await fetchData(attrAPI);
    let attrdata = data.data;
    let nextPage = data.nextPage;

    pageNumbers.shift();
    pageNumbers.push(nextPage);

    displayPage(attrdata);

    observer.observe(footer);
  } catch (error) {
    console.error("無法取得景點資料：", error);
  }
}

async function fetchNextPage() {
  try {
    let pageNumber = pageNumbers[0];
    let attrAPI = `${baseUrl}/attractions?page=${pageNumber}`;
    let data = await fetchData(attrAPI);
    let attrdata = data.data;
    let nextPage = data.nextPage;

    pageNumbers.shift();
    pageNumbers.push(nextPage);

    displayPage(attrdata);
  } catch (error) {
    console.error("無法取得新一頁景點資料：", error);
  }
}

async function fetchKeywordFirstPage(keyword) {
  try {
    let keyAPI = `${baseUrl}/attractions?page=0&keyword=${keyword}`;
    let data = await fetchData(keyAPI);
    let attrdata = data.data;
    let nextPage = data.nextPage;

    pageNumbers.shift();
    pageNumbers.push(nextPage);

    keywords.shift();
    keywords.push(keyword);

    const cardGrid = document.querySelector(".card-grid");
    while (cardGrid.firstChild) {
      cardGrid.removeChild(cardGrid.firstChild);
    }
    displayPage(attrdata);
    observer.observe(footer);
  } catch (error) {
    console.error("無法取得關鍵字景點資料：", error);
  }
}

async function fetchKeywordNextPage() {
  try {
    let pageNumber = pageNumbers[0];
    let keyword = keywords[0];
    let keyAPI = `${baseUrl}/attractions?page=${pageNumber}&keyword=${keyword}`;
    let data = await fetchData(keyAPI);
    let attrdata = data.data;
    let nextPage = data.nextPage;

    pageNumbers.shift();
    pageNumbers.push(nextPage);

    keywords.shift();
    keywords.push(keyword);

    displayPage(attrdata);
  } catch (error) {
    console.error("無法取得新一頁關鍵字景點資料：", error);
  }
}

// Search By Keyword
const searchBtn = document.getElementById("search-btn");
const searchInput = document.getElementById("search-input");

searchBtn.addEventListener("click", () => {
  goSeach();
});

searchInput.addEventListener("keyup", (e) => {
  if (e.key == "Enter") {
    goSeach();
  }
});

async function goSeach() {
  try {
    const searchInput = document.getElementById("search-input").value;
    fetchKeywordFirstPage(searchInput);
  } catch (error) {
    console.error("無法取得關鍵字景點資料：", error);
  }
}

// Display Data Card
async function displayPage(attrdata) {
  try {
    const cardGrid = document.querySelector(".card-grid");
    attrdata.forEach((attr) => {
      const card = createCardElement(attr);
      cardGrid.appendChild(card);
    });
  } catch (error) {
    console.error("無法顯示資料：", error);
  }
}

// Create Data Card
function createCardElement(card) {
  const cardTitleLength = 15;

  const cardGrid = document.querySelector(".card-grid");
  const cardContainer = document.createElement("div");
  cardContainer.setAttribute("class", "card-container");
  cardGrid.appendChild(cardContainer);

  const cardImg = document.createElement("div");
  cardImg.setAttribute("class", "card-img");
  cardImg.style.backgroundImage = `url(${card.images[0]})`;
  cardContainer.appendChild(cardImg);

  const cardTitle = document.createElement("div");
  cardTitle.setAttribute("class", "card-title");
  cardTitle.textContent = card.name;
  if (cardTitle.textContent.length > cardTitleLength) {
    cardTitle.textContent =
      cardTitle.textContent.slice(0, cardTitleLength) + "...";
  }
  cardImg.appendChild(cardTitle);

  const cardContent = document.createElement("div");
  cardContent.setAttribute("class", "card-content");
  cardContainer.appendChild(cardContent);

  const cardMrt = document.createElement("div");
  cardMrt.setAttribute("class", "card-mrt");
  cardMrt.textContent = card.mrt;
  cardContent.appendChild(cardMrt);

  const cardType = document.createElement("div");
  cardType.setAttribute("class", "card-type");
  cardType.textContent = card.category;
  cardContent.appendChild(cardType);

  // console.log(cardContainer);
  return cardContainer;
}

// Observer
const options = {
  root: null,
  rootMargin: "0px 0px 0px 0px",
  threshold: 1,
};

const footer = document.querySelector(".footer");
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      if (pageNumbers[0] !== null && keywords[0] == null) {
        fetchNextPage();
        return;
      } else if (pageNumbers[0] !== null && keywords[0] !== null) {
        fetchKeywordNextPage();
        return;
      } else {
        observer.unobserve(footer);
      }
    }
  });
}, options);

// Initialize Data
fetchTags();
fetchFirstPage();
