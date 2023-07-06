//console.log("EXECUTING");



/*
INDEX PAGE CHART  GET DATA FROM API

*/


window.onload = function () {
  var dps1 = [], dps2= [];
  var stockChart = new CanvasJS.StockChart("chartContainer",{
    theme: "light2",
    exportEnabled: true,
    title:{
      text:"IBM CHART with Date-Time Axis"
    },
    subtitles: [{
      text: "IBM PRICE IN RUPEES"
    }],
    charts: [{
      axisX: {
        crosshair: {
          enabled: true,
          snapToDataPoint: true
        }
      },
      axisY: {
        prefix: ""
      },
      data: [{
        type: "candlestick",
        yValueFormatString: "#,###.##",
        dataPoints : dps1
      }]
    }],
    navigator: {
      data: [{
        dataPoints: dps2
      }],
      slider: {
        minimum: new Date(2019, 12, 22),
        maximum: new Date(2021, 12, 24)
      }
    }
  });
  $.getJSON(baseUrl+"/api/get_stock_by_symbol?symbol=IBM", function(data) {
    x = Object.entries(data);
    mainData = Object.entries(x[1][1])

    for(var i = 0; i < mainData.length; i++){

      open = mainData[i][1]["Open"]
      high = mainData[i][1]["High"]
      low = mainData[i][1]["Low"]
      close = mainData[i][1]["Close"]


      dps1.push({x: new Date(mainData[i][0]), y: [Number(open), Number(high), Number(low), Number(close)]});
      dps2.push({x: new Date(mainData[i][0]), y: Number(close)});
    }
    stockChart.render();
  });
}



/*
END INDEX PAGE CHART  GET DATA FROM API
*/



/*
  BASE FILE TOP MARQUEE CONTENT AND TABLE CONTENT USING WEBSOCKET FOR REALTIME DATA

*/

const socket = new WebSocket('ws://127.0.0.1:8000/ws/get_stocks/');
    socket.onmessage = (e) => {
      var rcv_msg = e.data

      const da = JSON.parse(rcv_msg)

    ////////////////TOP marginQUEE DATA/////////////////
    var marku = document.getElementById("top_marquee");
    for(let i=0; i < da.length; i++){
      marku.innerHTML = marku.innerHTML + da[i].fields.name + " : " ;
      if(da[i].fields.previousClose < da[i].fields.lastPrice){
      marku.innerHTML = marku.innerHTML + '<span class="text-success">'  + da[i].fields.lastPrice +  '&nbsp;&nbsp;</span>';
      marku.innerHTML = marku.innerHTML + '<span class="fas fa-caret-up text-success" style="margin-right:25px"></span>'
      }
      else{
        marku.innerHTML = marku.innerHTML + '<span class="text-danger">'  + da[i].fields.lastPrice +  '&nbsp;&nbsp;</span>';
        marku.innerHTML = marku.innerHTML + '<span class="fas fa-caret-down text-danger" style="margin-right:25px"></span>'
      }
    }
      /////////////INSERT DATA IN TABLE/////////////////
      var table = document.getElementById("myTable");
      try{
        for(let i=0;i <= da.length;i++){
        table.deleteRow(-1);
        }
      }
      catch{
        let x=2;
      }
      try{
        var row = table.insertRow(-1);
        row.style.fontWeight="900";
        var cell1 = row.insertCell(0);
        var cell2 = row.insertCell(1);
        var cell3 = row.insertCell(2);
        var cell4 = row.insertCell(3);
        var cell5 = row.insertCell(4);
        var cell6 = row.insertCell(5);
        var cell7 = row.insertCell(6);
        var cell8 = row.insertCell(7);
        cell1.innerHTML = "Symbol";
        cell2.innerHTML = "Company name";
        cell3.innerHTML = "Price Change";
        cell4.innerHTML = "previous Close";
        cell5.innerHTML = "Day High";
        cell6.innerHTML = "Day Low";
        cell7.innerHTML = "Main Price";
        cell8.innerHTML = "Action";
        for(let i=0;i<da.length;i++){
          var row = table.insertRow(-1);
          var cell1 = row.insertCell(0);
          var cell2 = row.insertCell(1);
          var cell3 = row.insertCell(2);
          var cell4 = row.insertCell(3);
          var cell5 = row.insertCell(4);
          var cell6 = row.insertCell(5);
          var cell7 = row.insertCell(6);
          cell1.innerHTML = da[i].fields.symbol;
          cell2.innerHTML = da[i].fields.name;
          var cell8 = row.insertCell(7)
          if (da[i].fields.change > 0){
            cell3.style.color = 'green';
          }
          else{
            cell3.style.color = 'red';
          }
          cell3.innerHTML = da[i].fields.change + " %";
          cell4.innerHTML = da[i].fields.previousClose;
          cell5.innerHTML = da[i].fields.dayHigh;
          cell5.style.color = 'green'
          cell6.innerHTML = da[i].fields.dayLow;
          cell6.style.color = 'red';
          cell7.innerHTML = da[i].fields.lastPrice;
          if(cell7.innerHTML < cell4.innerHTML){
            cell7.style.color = "red";
          }
          else{
            cell7.style.color = 'green';
          }
          stock_detail_path = '/stock/'+ da[i].fields.symbol;
          cell8.innerHTML =  '<a class="btn btn-primary" href="' + stock_detail_path + '">VIEW DEATIL</a>';
        }
      }
      catch{
        
        let x=2;
      }

    }



    socket.onclose = (e) => {
        console.log("Socket closed!");
    }


/*
    END BASE FILE TOP MARQUEE CONTENT AND TABLE CONTENT USING WEBSOCKET FOR REALTIME DATA

*/








/*
STOCK DETAIL PAGE FETCH CHART AND INFORMATION THROUGH API

*/

  try{

    window.onload = function () {
      var symbol = document.getElementById("symbol").innerHTML

      var dps1 = [], dps2= [];
      var stockChart = new CanvasJS.StockChart("chartContainer",{
        theme: "light2",
        exportEnabled: true,
        title:{
          text: symbol + " CHART with Date-Time Axis"
        },
        subtitles: [{
          text: symbol + " PRICE IN RUPEES"
        }],
        charts: [{
          axisX: {
            crosshair: {
              enabled: true,
              snapToDataPoint: true
            }
          },
          axisY: {
            prefix: "₹"
          },
          data: [{
            type: "candlestick",
            yValueFormatString: "#,###.##",
            dataPoints : dps1
          }]
        }],
        navigator: {
          data: [{
            dataPoints: dps2
          }],
          slider: {
            minimum: new Date(2019, 12, 22),
            maximum: new Date(2021, 12, 24)
          }
        }
      });

      //bsestock
      //url = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=hdfc&apikey=AO48IFCXLA3BX1O9"

      url = baseUrl+"/api/get_stock_by_symbol?symbol=" + symbol
      $.getJSON(url, function(data) {
        x = Object.entries(data);
        mainData = Object.entries(x[1][1])

        for(var i = 0; i < mainData.length; i++){

          open = mainData[i][1]["Open"]
          high = mainData[i][1]["High"]
          low = mainData[i][1]["Low"]
          close = mainData[i][1]["Close"]


          dps1.push({x: new Date(mainData[i][0]), y: [Number(open), Number(high), Number(low), Number(close)]});
          dps2.push({x: new Date(mainData[i][0]), y: Number(close)});
        }
        stockChart.render();
      });
    }


  }
  catch{
    console.log("stock detail not loaded")
  }
    




 /*
    END STOCK DETAIL PAGE FETCH CHART AND INFORMATION THROUGH API
    
*/

    

    














