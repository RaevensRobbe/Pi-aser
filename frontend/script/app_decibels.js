'use strict';

let html_live_decibels;
let html_live_decibels_holder;

const IP = `${window.location.hostname}:5000`;

const getLiveDecibels = function(){
    console.info("Decibels ophalen uit JSON");
    const decibels = handleData(
      `http://${IP}/api/v1/decibelmeter/live`, 
       showLiveDecibels
    )
}

const showLiveDecibels = function(data){
    // console.log(data);
    let db_perc = data.DecibelWaarde / 1.20;
    //html_live_decibels_holder = `<H1>${data.DecibelWaarde} dB</H1>`;

    html_live_decibels_holder = 
    `<div class="single-chart">
      <svg viewBox="0 0 36 36" class="circular-chart blue">
        <path class="circle-bg"
          d="M18 2.0845
            a 15.9155 15.9155 0 0 1 0 31.831
            a 15.9155 15.9155 0 0 1 0 -31.831"
        />
        <path class="circle"
          stroke-dasharray="${db_perc}, 150"
          d="M18 2.0845
            a 15.9155 15.9155 0 0 1 0 31.831
            a 15.9155 15.9155 0 0 1 0 -31.831"
        />
        <text x="18" y="20.35" class="percentage">${data.DecibelWaarde} dB</text>
      </svg>
    </div>`;
  html_live_decibels.innerHTML = html_live_decibels_holder;
}

//#region ***  INIT / DOMContentLoaded  ***
const init_decibels = function () {
    html_live_decibels = document.querySelector(".js-decibels");
    if(html_live_decibels){
        setInterval(function(){getLiveDecibels()}, 1000);
    }
  }
  //#endregion
  
  document.addEventListener("DOMContentLoaded", init_decibels);