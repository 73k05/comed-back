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
                    let departmentAvailability = getDepartment(feature.properties.code, departmentAvailabilityList["departments"]);
                    let firstOpenSlot = "";
                    let isBookingOpen = false;
                    if (departmentAvailability) {
                        firstOpenSlot = departmentAvailability["bookingFirstOpenSlotDate"];
                        isBookingOpen = departmentAvailability["bookingOpen"];
                    }
                    var todayDate = new Date();
                    var twoWeeks = new Date();
                    var oneMonth = new Date();
                    var twoMonths = new Date();
                    twoWeeks.setDate(todayDate.getDate()+14);
                    oneMonth.setDate(todayDate.getDate()+30);
                    twoMonths.setDate(todayDate.getDate()+60);
                    var openSlotDate = Date.parse(firstOpenSlot);
                    // Book in 2 weeks
                    if (openSlotDate <= twoWeeks && isBookingOpen) {
                        return {color: "#9DE0AD"};
                    }
                    // Book between 2 weeks & 1 month
                    if ((openSlotDate > twoWeeks) && (openSlotDate <= oneMonth) && (isBookingOpen)) {
                        return {color: "#355C7D"};
                    }
                    // Book in 2 months
                    if (openSlotDate >= twoMonths && isBookingOpen) {
                        return {color: "#F26B38"};
                    }
                    //Booking closed
                    return {color: "#FE4365"};
                }, onEachFeature: onEachFeature
            }).addTo(map);

            //Bind popup to display name & availability
            function onEachFeature(feature, layer) {
                const departmentAvailability = getDepartment(feature.properties.code, departmentAvailabilityList["departments"]);
                let popupText = `<p><b> ${feature.properties.nom} (${feature.properties.code})</b><br/>`;
                let firstOpenSlot = departmentAvailability ? departmentAvailability["bookingFirstOpenSlotDate"] : "";
                if (firstOpenSlot) {
                    console.log(firstOpenSlot);
                    firstOpenSlot = new Date(firstOpenSlot);
                    firstOpenSlot = ((firstOpenSlot.getDate() > 9) ? firstOpenSlot.getDate() : ('0' + firstOpenSlot.getDate())) + '/' + ((firstOpenSlot.getMonth() > 8) ? (firstOpenSlot.getMonth() + 1) : ('0' + (firstOpenSlot.getMonth() + 1))) + '/' + firstOpenSlot.getFullYear();
                }
                if (firstOpenSlot && departmentAvailability["bookingOpen"] === true) {
                    popupText = `${popupText}<b style='color:#78995D;'>Ouvert</b> prochain créneau le <b>${firstOpenSlot}</b></p>`;
                } else if (firstOpenSlot) {
                    popupText = `${popupText}<b style='color:#28499B;'>Fermé</b>  prochain créneau le <b>${firstOpenSlot}</b></p>`;
                } else {
                    popupText = `${popupText}<b style='color:#ff0000;'>Fermé</b></p>`;
                }
                var departmentBookUrl = departmentAvailability ? departmentAvailability["departmentBookUrl"] : "";
                popupText = `${popupText}<p> Réserver sur <b><a href='./index.html'>CoMed</a></b><br/>`;
                popupText = `${popupText}Réserver sur <a href='${departmentBookUrl}' target='_blank'>gouv</a></p>`;
                layer.bindPopup(popupText);
            }
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