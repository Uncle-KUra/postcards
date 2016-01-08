#!/usr/bin/env python3
# encoding: utf-8

_author__ = 'uncle.kura@yandex.ru'

import operator
from postcards_db import DB

PART_1 = '''
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
      html { height: 100%; width: 100% }
      body { height: 100%; width: 100%; margin: 0; padding: 0 }
      #map-canvas { height: 100%; width: 100% }
    </style>
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyCU4giTcNZxOTDfpFIPPtS-Z3X_g6kjA9s&sensor=true">
    </script>
    <script type="text/javascript">
      function initialize() {
        var mapOptions = {
          center: new google.maps.LatLng(60, 30),
          zoom: 4,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        var map = new google.maps.Map(document.getElementById("map-canvas"),
            mapOptions);

		var marker = new google.maps.Marker( {position: new google.maps.LatLng(0, 0), map: map});

		var output = document.getElementById("output");


  		google.maps.event.addListener(map, 'click', function(e) {
    		placeMarker(e.latLng, map, marker);
  		});
      }

function distance(pos1, pos2){
    var deg2rad = Math.PI / 180.0;
    var lat1 = pos1.lat() * deg2rad;
    var lat2 = pos2.lat() * deg2rad;
    var lon1 = pos1.lng() * deg2rad;
    var lon2 = pos2.lng() * deg2rad;

    return 6371110 * Math.acos(Math.sin(lat1) * Math.sin(lat2)
            + Math.cos(lat1) * Math.cos(lat2) * Math.cos(lon1 - lon2));

}

function placeMarker(position, map, marker) {
  marker.setPosition(position);
  document.getElementById("coordsF").value = "" + position.lat() + ";" + position.lng();
}

google.maps.event.addDomListener(window, 'load', initialize);

function cityChanged(){
    document.getElementById("cityF").value = city.value;
}

function jpegChanged(){
    document.getElementById("jpegName").value = jpeg.value;
}


function dateChanged(){
	var d = new Date(dateFrom.value);
	var d2 = new Date(dateTo.value);
	var d3 = d2.getTime() - d.getTime();
	var day = d.getDate();
	var month = d.getMonth()+1;
	document.getElementById("date0F").value = day + "." + month + "." + d.getFullYear();
	document.getElementById("date1F").value = d2.getDate() + "." + (d2.getMonth() + 1) + "." + d2.getFullYear();

}

function addOnClick(){
    //var mydoc = window.open( "data:application/download;charset=utf-8;base64," + btoa("123"));
    //var myCsv = "Col1,Col2,Col3\\nval1,val2,val3";
    //window.open('data:text/csv;charset=utf-8,' + escape(myCsv));
    var output = {};
    output['city'] = document.getElementById("cityF").value;
    output['dateFrom'] = document.getElementById("date0F").value;
    output['dateTo'] = document.getElementById("date1F").value;
    output['coords'] = document.getElementById("coordsF").value;
    output['senders'] = document.getElementById("sendersF").value;
    output['jpeg'] = document.getElementById("jpegName").value;
   text = JSON.stringify(output);
   name = "postcard" + output['dateFrom'] + "--" + Math.random() + ".json";
   type = "text/plain";

    var a = document.createElement("a");
    var file = new Blob([text], {type: type});
    a.href = URL.createObjectURL(file);
    a.download = name;
    a.click();
}

function checkChanged(){
	var i = 1;
	var check = document.getElementById("ch" + String(i));
	var checkSender = document.getElementById("chText" + String(i));
	var n = 0
	var oneText = "";
	while (check != null)
	{
		if (check.checked)
		{
			n++;
    		oneText = oneText + checkSender.innerHTML + ",";
		}
		i++;
		check = document.getElementById("ch" + String(i));
		checkSender = document.getElementById("chText" + String(i));
	}
	document.getElementById("sendersF").value = oneText;
}


window.onload = function () {
	var today = (new Date()).toJSON().slice(0,10);;
	document.getElementById("dateTo").value = 	today;
	document.getElementById("dateFrom").value = 	today;
}
    </script>
  </head>
  <body>
	<table  style="width:100%;height:100%">
	<tr style="height:500">
		<td style="width:50%">
    		<div id="map-canvas" style="height:500"></div>
		</td>
		<td style="width: 50%">
			<div><input type="date" id="dateFrom" onChange="dateChanged();"></div>
			<div><input type="date" id="dateTo" onChange="dateChanged();"></div>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
			<br>
            <div> jpeg <input type="file" onChange="jpegChanged();" id="jpeg" name="jpeg">
            <div> Город <select name="city" id="city" onChange="cityChanged();">

'''

PART_2 = '''
                       </select>
            </div>
		</td>
	</tr>
	<tr style="height:30%">
		<td style="width:50%">
'''

PART_3 = '''
		</td>
		<td style="width:50%">

    <form action="/add_card" method="post">
        <div> Город <input type="text" name="cityF" id="cityF"></div>
        <div> Отправлено <input type="text" name="date0F" id="date0F"></div>
        <div> Получено <input type="text" name="date1F" id="date1F"></div>
        <div> Координаты <input type="text" name="coordsF" id="coordsF"></div>
        <div> Отправители <input type="text" name="sendersF" id="sendersF"></div>
        <div> jpeg <input type="text" name="jpegName" id="jpegName"></div>
      <div><input type="submit"></div>
    </form>
		</td>
	</tr>
	</table>
  </body>
</html>
'''


def print_city_list():
    s = ''
    with DB() as db:
        for city in sorted(db.get_cities(), key=operator.attrgetter('name')):
            s += '<option value="' + city.name + '">' + city.name + '</option>'
    return s


def print_sender_list():
    s = ''
    with DB() as db:
        i = 1
        for sender in sorted(db.get_senders(), key=operator.attrgetter('name')):
            s += '<div><input type="checkBox" id="ch' + \
                 str(i) + '" onChange="checkChanged();"><div id="chText' + str(i) + '">' + sender.name + \
                 '</div></input></div>'
            i += 1
    return s


def generate_add_html():
    s = PART_1
    s += print_city_list()
    s += PART_2
    s += print_sender_list()
    s += PART_3
    return  s


if __name__ == '__main__':
    print(generate_add_html())
