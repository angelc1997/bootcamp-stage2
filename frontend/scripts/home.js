// 執行TypingEffect
const typedTextSpan = document.querySelector(".typing-text");
// const cursorSpan = document.querySelector(".typing-cursor");
const textArray = ["規劃北台灣之旅", "預訂專業導覽", "支付快速完成"];
let textArrayIndex = 0;
let charIndex = 0;

function type() {
  if (charIndex < textArray[textArrayIndex].length) {
    typedTextSpan.textContent = textArray[textArrayIndex].slice(
      0,
      charIndex + 1
    );
    charIndex++;
    setTimeout(type, 200);
  } else {
    setTimeout(erase, 1000);
  }
}

function erase() {
  if (charIndex > 0) {
    typedTextSpan.textContent = textArray[textArrayIndex].slice(
      0,
      charIndex - 1
    );
    charIndex--;
    setTimeout(erase, 200);
  } else {
    textArrayIndex++;
    if (textArrayIndex >= textArray.length) {
      textArrayIndex = 0;
    }
    setTimeout(type, 1000);
  }
}

document.addEventListener("DOMContentLoaded", function () {
  if (textArray.length > 0) {
    type();
  }
});

//  Tablist function
const tabObject = {
  0: {
    title: "探索北台灣",
    description: "瀏覽熱門捷運站周邊景點",
    img: "/assets/svg/tab0.svg",
  },
  1: {
    title: "訂製專屬旅程",
    description: "根據興趣和時間選擇適合的一日遊行程",
    img: "/assets/svg/tab1.svg",
  },

  2: {
    title: "預訂導覽",
    description: "選擇喜歡的導覽方案，確保最佳旅程",
    img: "/assets/svg/tab2.svg",
  },

  3: {
    title: "線上支付",
    description: "線上付款，方便快捷",
    img: "/assets/svg/tab3.svg",
  },

  4: {
    title: "開始探索",
    description: "開啟您的北台灣精彩之旅",
    img: "/assets/svg/tab4.svg",
  },
};

function showTab(index) {
  const tabContent = document.querySelector(".tabcontent");

  tabContent.innerHTML = "";

  const tabDescription = document.createElement("div");
  tabDescription.classList.add("tabdescription");

  const h1 = document.createElement("h1");
  h1.textContent = tabObject[index].title;

  const p = document.createElement("p");
  p.textContent = tabObject[index].description;

  const img = document.createElement("img");
  img.src = tabObject[index].img;

  tabDescription.appendChild(h1);
  tabDescription.appendChild(p);
  tabContent.appendChild(tabDescription);
  tabContent.appendChild(img);
}

//  呼叫AOS
AOS.init();
