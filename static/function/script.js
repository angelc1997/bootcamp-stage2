const mrtAPI = "http://127.0.0.1:8000/api/mrts";
const attrAPI = "http://127.0.0.1:8000/api/attractions?page=0";

fetchTags();
fetchAttr();

async function fetchTags() {
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
  clickTag.forEach((tag) => {
    tag.addEventListener("click", () => {
      // console.log(tag.textContent);
      document.getElementById("search-input").value = tag.textContent;
    });
  });
}

const tags = document.querySelector(".tag-list");
const icons = document.querySelectorAll(".tag-icon i");

icons.forEach((icon) => {
  icon.addEventListener("click", () => {
    // console.log(icon.id);
    tags.scrollLeft += icon.id === "next" ? 600 : -600;
  });
});

async function fetchAttr() {
  const response = await fetch(attrAPI, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }

  const data = await response.json();
  const attrdata = data.data;

  console.log(attrdata);

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
}
