TPDirect.setupSDK(
  151732,
  "app_8IDBjVYv7MBtN0Lq6WeXJzGg39TFVhxEn0L7wwhGclxF6c63fSk7qXvY2v32",
  "sandbox"
);

TPDirect.card.setup({
  fields: {
    number: {
      element: document.getElementById("card-number"),
      placeholder: "**** **** **** ****",
    },
    expirationDate: {
      element: document.getElementById("card-expiration-date"),
      placeholder: "MM / YY",
    },
    ccv: {
      element: document.getElementById("card-ccv"),
      placeholder: "ccv",
    },
  },
  styles: {
    input: {
      color: "gray",
    },
    ".valid": {
      color: "green",
    },
    ".invalid": {
      color: "red",
    },
    "@media screen and (max-width: 400px)": {
      input: {
        color: "orange",
      },
    },
  },
  isMaskCreditCardNumber: true,
  maskCreditCardNumberRange: {
    beginIndex: 6,
    endIndex: 11,
  },
});

TPDirect.card.onUpdate(function (update) {
  const submitButton = document.getElementById("submit-button");
  if (update.canGetPrime) {
    submitButton.removeAttribute("disabled");
  } else {
    submitButton.setAttribute("disabled", true);
  }
});

document
  .getElementById("submit-button")
  .addEventListener("click", async function (event) {
    event.preventDefault();

    const tappayStatus = TPDirect.card.getTappayFieldsStatus();
    if (tappayStatus.canGetPrime === false) {
      alert("無法獲得，請確認填寫完整資訊");
      return;
    }

    TPDirect.card.getPrime(async (result) => {
      if (result.status !== 0) {
        console.log("Get prime error: " + result.msg);
        return;
      }
      console.log("Get prime success, prime: " + result.card.prime);

      const contactName = document.getElementById("contact-name").value;
      const contactEmail = document.getElementById("contact-email").value;
      const contactPhone = document.getElementById("contact-phone").value;

      const token = localStorage.getItem("token");
      const tripData = JSON.parse(localStorage.getItem("bookingData"));

      console.log(tripData);
      console.log(tripData.data.attraction);
      const attraction = tripData.data.attraction;
      const date = tripData.data.date;
      const time = tripData.data.time;
      const price = tripData.data.price;

      const requestBody = JSON.stringify({
        prime: result.card.prime,
        order: {
          price: price,
          trip: {
            attraction: {
              id: attraction.id,
              name: attraction.name,
              address: attraction.address,
              image: attraction.image,
            },
            date: date,
            time: time,
          },
          contact: {
            name: contactName,
            email: contactEmail,
            phone: contactPhone || null,
          },
        },
      });

      try {
        const response = await fetch(`${baseUrl}/orders`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: requestBody,
        });

        if (!response.ok) {
          throw new Error(`Error: ${response.status}`);
        }

        const responseData = await response.json();
        console.log("Response data:", responseData);

        orderNumber = responseData.data.number;

        window.location.href = `/thankyou?order=${orderNumber}`;

        // alert("訂單提交成功！");
      } catch (error) {
        console.error(error);
        alert("訂單提交失敗!");
      }
    });
  });
