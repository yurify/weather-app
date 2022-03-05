/* Handle the burger menu bar */

const burgerIcon = document.querySelector(".burger-icon");
const burgerMenu = document.querySelector(".menu");

burgerIcon.addEventListener("click", displayMenu);

function displayMenu() {
  if (burgerMenu.style.display === "flex") {
    burgerMenu.style.display = "none";
  } else {
    burgerMenu.style.display = "flex";
  }
}

/* AJAX temperature update */

// function updateAllCards() {
//     /* Update the temperature only if the tab is active in a browser. */
//     console.log('Temperature updated on all cards.');
//     if (!document.hidden) {
//         const cityCards = document.querySelectorAll(".pro-city-block");
//         cityCards.forEach(cityCard => updateCityWeather(cityCard));
//     }
// }

function update() {
  if (!document.hidden) {
    let cityNamesNodeList = document.querySelectorAll(".city-name");
    const cityNames = [];
    cityNamesNodeList.forEach((cityName) => cityNames.push(cityName.innerText));
    console.log(cityNames);
    let temperatures = document.getElementsByClassName("city-weather-temp-pro");
    let url = "/weatherpro/updatio/" + cityNames.toString();

    // create XHR and send the array of city names

    let xhr = new XMLHttpRequest();
    xhr.responseType = "json";
    xhr.onload = function () {
      if (this.status == 200) {
        // console.log(xhr.response);
        for (let i = 0; i < temperatures.length; i++) {
          let newTemp = xhr.response[i].toFixed(1).toString();
          if (newTemp > 0) {
            temperatures[i].innerText = "+" + newTemp + "°";
          } else {
            temperatures[i].innerText = newTemp + "°";
          }
        }
      }
    };

    xhr.open("GET", url);
    xhr.send();
  }
  console.log("Temperature updated on all cards.");
}

window.onload = () => {
  console.log("The page has been loaded.");
  myInterval = window.setInterval(update, 10000); // update the temperature every 10 seconds
};
