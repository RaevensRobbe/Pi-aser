'use strict';

const lanIP = `${window.location.hostname}:5000`; //Normaal
// const lanIP = `${window.location.hostname}:5500`; //Liveserver
const socket = io(`http://${lanIP}`);

const getPlayTimeData = function(ID){
  console.info("Historiek ophalen uit JSON");
  const elementByType = handleData(
    `http://${lanIP}/api/v1/playhistory/${ID}`,
    showPlayTimeData
  )
}

const showPlayTimeData = function(data){

  console.log(data);

  let converted_labels = [];
  let converted_data = [];
  let speeltijd;
  for (const time of data){
/*      if(time.Playtime == null){
        let speeltijd = "00:00"
      }
      else{*/
        let tijd = time.PlayTime;
        let uren =  parseInt(tijd.substring(0, 2)) * 60;
        let minuten = parseInt(tijd.substring(4, 5));
        let seconden = parseInt(tijd.substring(7,8));
        let speeltijd = uren + minuten;
     // }
        let datumsub = time.Datum;
        let correctedatum = datumsub.substring(5, 25);
      
      converted_labels.push(correctedatum);
      converted_data.push(speeltijd);
  };

  console.log(converted_data);
  console.log(converted_labels);

  drawChart(converted_labels, converted_data);
}

const drawChart = function(labels, playtime){
    let ctx = document.getElementById('myChart').getContext('2d');

    var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
    gradientStroke.addColorStop(0, "#E92330");
    gradientStroke.addColorStop(1, "#830A13");

    let config = {
        type: 'line',
        data: {
            labels: labels,
            datasets: [ 
                {
                label : 'Time played',
                fontColor: 'white',
                borderColor:               gradientStroke,
                pointBorderColor:          gradientStroke,
                pointBackgroundColor:      gradientStroke,
                pointHoverBackgroundColor: gradientStroke,
                pointHoverBorderColor:     gradientStroke,
                pointBorderWidth: 10,
                pointHoverRadius: 10,
                pointHoverBorderWidth: 1,
                pointRadius: 3,
                fill: false,
                borderWidth: 4,
                data: playtime, //Playtime
                }
            ]
        },
    options : {
        responsive: true,
        title: {
            //fontColor: 'white',
            display: true,
            text: 'Playtime last 7 times'
        },
        tooltips:{
            mode: 'index',
            intersect: true
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales:{
            xAxes:[
                {
                display: true,
                gridLines:{
                  display: true,
                  //color:'#a8a3a3'
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Date',
                    //fontColor: 'white'
                },
                ticks : {
                  minRotation : 45,
                  maxTicksLimit: 10,
                  //fontColor: 'white'
                }
            }
            ],
            yAxes: [
                {
                    display: true,
                    gridLines:{
                      display: true,
                      //color:'#a8a3a3'
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Time in minutes',
                        //fontColor: 'white'
                    },
                    ticks : {
                      beginAtZero: true,
                      stepSize: 15,
                      suggestedMax: 120,
                      //fontColor: 'white',
                    }
                }
            ]
        }
    }
};

    let myChart = new Chart(ctx, config);
}

const listenToUI = function () {
    const knoppen = document.querySelectorAll(".js-sound-btn");
    for (const knop of knoppen) {
      knop.addEventListener("click", function () {
        const id = this.dataset.idsound;
        console.log(id);

        socket.emit("F2B_select_sound", { selected_sound: id });
        console.log("changed sound");
      });
    }
  };

//#region ***  INIT / DOMContentLoaded  ***
const init = function (){
    listenToUI()
    getPlayTimeData(1);
}
//#endregion

document.addEventListener("DOMContentLoaded", init);
