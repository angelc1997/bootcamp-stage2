// Draggable Tags Function

async function fetchTags() {
  let mrtAPI = "http://127.0.0.1:8000/api/mrts";
  const response = await fetch(mrtAPI, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }

  const data = await response.json();
  for (let i = 0; i < Object.values(data.data).length; i++) {
    const tags = document.querySelector(".tag-list");
    let tag = document.createElement("div");
    tag.setAttribute("class", "tag");
    tag.textContent = Object.values(data.data)[i];
    tags.appendChild(tag);
  }

  const clickTag = document.querySelectorAll(".tag");
  const searchInput = document.getElementById("search-input");
  clickTag.forEach((tag) => {
    tag.addEventListener("click", () => {
      // console.log(tag.textContent);
      searchInput.classList.add("searching");
      document.getElementById("search-input").value = tag.textContent;
    });
  });
}

// Tags Dragging
const tags = document.querySelector(".tag-list");
const icons = document.querySelectorAll(".tag-icon");

icons.forEach((icon) => {
  icon.addEventListener("click", () => {
    tags.scrollLeft += icon.id === "next" ? 600 : -600;
  });
});

// Fetch Attractions
let firstPage = "http://127.0.0.1:8000/api/attractions?page=0";
let pages = [];
async function fetchAttr() {
  const response = await fetch(firstPage, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }

  let data = await response.json();
  let attrdata = data.data;
  let nextPage = data.nextPage;

  // 把下一頁存到陣列中
  pages.push(nextPage);

  // 顯示第一頁
  for (let i = 0; i < attrdata.length; i++) {
    const cardGrid = document.querySelector(".card-grid");
    const cardContainer = document.createElement("div");
    cardContainer.setAttribute("class", "card-container");
    cardGrid.appendChild(cardContainer);

    const cardImg = document.createElement("div");
    cardImg.setAttribute("class", "card-img");
    cardImg.style.backgroundImage = `url(${attrdata[i].images[0]})`;
    cardContainer.appendChild(cardImg);

    const cardTitle = document.createElement("div");
    cardTitle.setAttribute("class", "card-title");
    cardTitle.textContent = attrdata[i].name;
    let cardTitleLength = 15;
    let cardTitleText = cardTitle.textContent;

    if (cardTitle.textContent.length > cardTitleLength) {
      cardTitle.textContent = cardTitleText.slice(0, cardTitleLength) + "...";
    }

    cardImg.appendChild(cardTitle);

    const cardContent = document.createElement("div");
    cardContent.setAttribute("class", "card-content");
    cardContainer.appendChild(cardContent);

    const cardMrt = document.createElement("div");
    cardMrt.setAttribute("class", "card-mrt");
    cardMrt.textContent = attrdata[i].mrt;
    cardContent.appendChild(cardMrt);

    const cardType = document.createElement("div");
    cardType.setAttribute("class", "card-type");
    cardType.textContent = attrdata[i].category;
    cardContent.appendChild(cardType);
  }

  observer.observe(footer);
}

fetchTags();
fetchAttr();

async function fetchNextPage(index) {
  let pageUrl = "http://127.0.0.1:8000/api/attractions?page=";
  let nextUrl = pageUrl + index;

  try {
    const response = await fetch(nextUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    let data = await response.json();
    let attrdata = data.data;
    let nextPage = data.nextPage;

    pages.shift();
    // console.log(pages);
    // 把下一頁存到陣列中
    pages.push(nextPage);
    console.log(pages);

    // 顯示下一頁
    for (let i = 0; i < attrdata.length; i++) {
      const cardGrid = document.querySelector(".card-grid");
      const cardContainer = document.createElement("div");
      cardContainer.setAttribute("class", "card-container");
      cardGrid.appendChild(cardContainer);

      const cardImg = document.createElement("div");
      cardImg.setAttribute("class", "card-img");
      cardImg.style.backgroundImage = `url(${attrdata[i].images[0]})`;
      cardContainer.appendChild(cardImg);

      const cardTitle = document.createElement("div");
      cardTitle.setAttribute("class", "card-title");
      cardTitle.textContent = attrdata[i].name;
      let cardTitleLength = 15;
      let cardTitleText = cardTitle.textContent;

      if (cardTitle.textContent.length > cardTitleLength) {
        cardTitle.textContent = cardTitleText.slice(0, cardTitleLength) + "...";
      }

      cardImg.appendChild(cardTitle);

      const cardContent = document.createElement("div");
      cardContent.setAttribute("class", "card-content");
      cardContainer.appendChild(cardContent);

      const cardMrt = document.createElement("div");
      cardMrt.setAttribute("class", "card-mrt");
      cardMrt.textContent = attrdata[i].mrt;
      cardContent.appendChild(cardMrt);

      const cardType = document.createElement("div");
      cardType.setAttribute("class", "card-type");
      cardType.textContent = attrdata[i].category;
      cardContent.appendChild(cardType);
    }
    if (!nextPage) {
      console.log("no more pages");
      return;
    }
  } catch (error) {
    console.log(error);
  }
}

const options = {
  root: null,
  rootMargin: "0px 0px 0px 0px",
  threshold: 1,
};

const footer = document.querySelector(".footer");
const grid = document.querySelector(".card-grid");

// const NoKeywordobserver = new IntersectionObserver((entries) => {
//   entries.forEach((entry) => {
//     console.log(entry);

//     if (pages[0] == null) {
//       console.log("已經到底囉");
//       NoKeywordobserver.unobserve(footer);
//     } else if (entry.isIntersecting) {
//       fetchNextPage(pages[0]);
//     }
//   });
// }, options);

const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");

let keywordPages = [];
let keyword = [];

// const observer = new IntersectionObserver((entries) => {
//   entries.forEach((entry) => {
//     if (keywordPages[0] == null) {
//       console.log("沒有更多頁囉");
//       observer.unobserve(footer);
//     } else if (entry.isIntersecting) {
//       fetchNextKeyword(keywordPages[0]);
//     }
//   });
// }, options);

const lastCard = document.querySelector(".card-grid .last-card");

async function fetchKey(keyAPI) {
  const response = await fetch(keyAPI, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }

  let data = await response.json();
  let attrdata = data.data;
  let nextPage = data.nextPage;
  pages.shift();
  pages.push(nextPage);

  // 清除首頁
  const cardGrid = document.querySelector(".card-grid");
  while (cardGrid.firstChild) {
    cardGrid.removeChild(cardGrid.firstChild);
    observer.unobserve(footer);
  }

  for (let i = 0; i < attrdata.length; i++) {
    const cardGrid = document.querySelector(".card-grid");
    const cardContainer = document.createElement("div");
    cardContainer.setAttribute("class", "card-container");
    cardGrid.appendChild(cardContainer);

    const cardImg = document.createElement("div");
    cardImg.setAttribute("class", "card-img");
    cardImg.style.backgroundImage = `url(${attrdata[i].images[0]})`;
    cardContainer.appendChild(cardImg);

    const cardTitle = document.createElement("div");
    cardTitle.setAttribute("class", "card-title");
    cardTitle.textContent = attrdata[i].name;
    let cardTitleLength = 15;
    let cardTitleText = cardTitle.textContent;

    if (cardTitle.textContent.length > cardTitleLength) {
      cardTitle.textContent = cardTitleText.slice(0, cardTitleLength) + "...";
    }

    cardImg.appendChild(cardTitle);

    const cardContent = document.createElement("div");
    cardContent.setAttribute("class", "card-content");
    cardContainer.appendChild(cardContent);

    const cardMrt = document.createElement("div");
    cardMrt.setAttribute("class", "card-mrt");
    cardMrt.textContent = attrdata[i].mrt;
    cardContent.appendChild(cardMrt);

    const cardType = document.createElement("div");
    cardType.setAttribute("class", "card-type");
    cardType.textContent = attrdata[i].category;
    cardContent.appendChild(cardType);
  }
  observer.observe(footer);
  return searchInput;
}

searchBtn.addEventListener("click", async () => {
  const searchInput = document.getElementById("search-input").value;
  let keyAPI = `http://127.0.0.1:8000/api/attractions?page=0&keyword=${searchInput}`;
  await fetchKey(keyAPI);
  console.log(fetchKey(keyAPI));
  keyword.push(searchInput);
});

async function fetchNextKeyword(nextPage) {
  const searchInput = keyword[0];
  let pageUrl = `http://127.0.0.1:8000/api/attractions?page=${nextPage}&keyword=${searchInput}`;

  console.log(pageUrl);
  try {
    const response = await fetch(pageUrl, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (!response.ok) {
      throw new Error(`Error: ${response.status}`);
    }

    let data = await response.json();
    let attrdata = data.data;
    let nextPage = data.nextPage;

    pages.shift();
    // console.log(pages);
    // 把下一頁存到陣列中
    pages.push(nextPage);
    console.log(pages);

    // 顯示下一頁
    for (let i = 0; i < attrdata.length; i++) {
      const cardGrid = document.querySelector(".card-grid");
      const cardContainer = document.createElement("div");
      cardContainer.setAttribute("class", "card-container");
      cardGrid.appendChild(cardContainer);

      const cardImg = document.createElement("div");
      cardImg.setAttribute("class", "card-img");
      cardImg.style.backgroundImage = `url(${attrdata[i].images[0]})`;
      cardContainer.appendChild(cardImg);

      const cardTitle = document.createElement("div");
      cardTitle.setAttribute("class", "card-title");
      cardTitle.textContent = attrdata[i].name;
      let cardTitleLength = 15;
      let cardTitleText = cardTitle.textContent;

      if (cardTitle.textContent.length > cardTitleLength) {
        cardTitle.textContent = cardTitleText.slice(0, cardTitleLength) + "...";
      }

      cardImg.appendChild(cardTitle);

      const cardContent = document.createElement("div");
      cardContent.setAttribute("class", "card-content");
      cardContainer.appendChild(cardContent);

      const cardMrt = document.createElement("div");
      cardMrt.setAttribute("class", "card-mrt");
      cardMrt.textContent = attrdata[i].mrt;
      cardContent.appendChild(cardMrt);

      const cardType = document.createElement("div");
      cardType.setAttribute("class", "card-type");
      cardType.textContent = attrdata[i].category;
      cardContent.appendChild(cardType);
    }
    if (!nextPage) {
      console.log("沒有更多頁囉");
      return;
    }
  } catch (error) {
    console.log(error);
  }
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    console.log(entry);
    if (entry.isIntersecting) {
      if (pages[0] == null && keyword[0] == null) {
        console.log("沒有更多頁囉");
        observer.unobserve(footer);
        return;
      } else if (pages[0] !== null && keyword[0] == null) {
        fetchNextPage(pages[0]);
      } else if (pages[0] == null && keyword[0] !== null) {
        fetchKey(pages[0]);
      } else if (pages[0] !== null && keyword[0] !== null) {
        fetchNextKeyword(pages[0]);
      }
      return;
    }
  });
}, options);
