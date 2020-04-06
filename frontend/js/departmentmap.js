(function () {
    'use strict';
    var map = L.map('mapid').setView([45.7741, 3.0605], 6);
    L.tileLayer('https://api.mapbox.com/styles/v1/73k05/ck8kdu10z0bnp1jmnatgfhyt7/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiNzNrMDUiLCJhIjoiY2s4a2FwM3FzMGcyMjNtcXEzYWpydzFjMiJ9.lIIsNlB9khxZUlmmkp8f9Q', {
        maxZoom: 18,
        id: 'ck8kdu10z0bnp1jmnatgfhyt7',
        tileSize: 512,
        zoomOffset: -1
    }).addTo(map);
    //GEt dep availability list
    $.getJSON("./resources/json/departmentavailabilities.json", function (departmentAvailabilityList) {
        //Get dep list in map
        $.getJSON("./resources/depmaps/departements.geojson", function (departmentJson) {
            L.geoJSON(departmentJson, {
                style: function (feature) {
                    var departmentAvailability = getDepartment(feature.properties.code, departmentAvailabilityList["departments"]);
                    var firstOpenSlot = departmentAvailability ? departmentAvailability["bookingFirstOpenSlotDate"] : "";
                    var todayDate = new Date();
                    var openSlotDate = Date.parse(firstOpenSlot);
                    if (openSlotDate >= todayDate) {
                        return {color: "#78995D"};
                    } else {
                        //Booking closed
                        return {color: "#ff0000"};
                    }
                }
            }).addTo(map);
        });
    });
})();

function getDepartment(departmentCode, departmentList) {
    var departmentToReturn;
    $.each(departmentList, function (index, department) {
        if (parseInt(department.departmentCode) === parseInt(departmentCode)) {
            departmentToReturn = department;
            return department
        }
    });
    return departmentToReturn;
}

//TODO: Bind popup to display name & availability
// function onEachFeature(feature, layer) {
//     // layer.bindPopup(feature.properties.popupContent);
//     // layer.setbindPopup(feature.properties.popupContent);
// }