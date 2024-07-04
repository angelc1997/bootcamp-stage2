window.onload = async function () {
  const token = localStorage.getItem("token");
  if (!token) {
    window.location.href = "http://127.0.0.1:8000/";
  } else {
    showLogoutButton();
  }

  const newUrl = new URLSearchParams(window.location.search);
  const orderNumber = newUrl.get("order");
  console.log(orderNumber);

  const orderAPI = `http://127.0.0.1:8000/api/order/${orderNumber}`;

  const response = await fetch(orderAPI, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error(`Error: ${response.status}`);
  }

  const data = await response.json();
  console.log(data);

  createPaymentList(data);
};

function createPaymentList(data) {
  const payID = document.getElementById("pay-id");
  payID.textContent = data.data.number;

  const payName = document.getElementById("pay-name");
  payName.textContent = data.data.trip.contact.name;

  const payPhone = document.getElementById("pay-phone");
  payPhone.textContent = data.data.trip.contact.phone;

  const payEmail = document.getElementById("pay-email");
  payEmail.textContent = data.data.trip.contact.email;

  const payDate = document.getElementById("pay-date");
  payDate.textContent = data.data.trip.date;

  const payTime = document.getElementById("pay-time");

  let time = (data.data.trip.time = "morning"
    ? "早上9點到下午3點"
    : "下午3點到晚上9點");
  payTime.textContent = time;

  const payAttr = document.getElementById("pay-attr");
  payAttr.textContent = data.data.trip.attraction.name;

  const payPrice = document.getElementById("pay-price");
  payPrice.textContent = data.data.price;

  const overlay = document.querySelector(".overlay");
  overlay.style.display = "none";

  const loader = document.querySelector(".loader");
  loader.style.display = "none";

  localStorage.removeItem("bookingData");
}
