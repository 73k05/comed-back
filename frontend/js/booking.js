(function () {
    'use strict';
    window.addEventListener('load', function () {
        initEventListener();
        populateSelect();
        initBookDatePickers();
        addressAutoComplete();

    }, false);
})();

// Display Booking Date
function initBookDatePickers() {
    // Calculating the actual day date + 6 days ahead
    let nextWeekDate = new Date();
    nextWeekDate.setDate(nextWeekDate.getDate() + minimumDelayBook);
    $("#bookingDatePicker").datepicker({
        onSelect: function (date) {
        },
        format: "dd/mm/yyyy",
        startDate: nextWeekDate,
        firstDay: 1,
    });

    // Calculating the actual day date - 18 years behind
    let minBirthDate = new Date()
    minBirthDate.setFullYear(new Date().getFullYear() - 18);
    $("#birthdate").datepicker({
        onSelect: function (date) {
        },
        format: "dd/mm/yyyy",
        endDate: minBirthDate,
        firstDay: 1,
    });
}

function getTemplate() {
    return 'commissionmedicale_template';
}

function getParams(form) {
    return {
        email: form.email.value,
        firstname: form.firstname.value,
        lastname: form.lastname.value,
        phone: form.phone.value,
        number: Math.random() * 100000 | 0,
        birthdate: form.birthdate.value,
        birthname: form.birthname.value,
        region: form.region.value,
        typevisit: form.typevisit.value,
        bookingChooseDate: form.bookingdate.value,
        bookedCurrentDate: "",
        addressStreet: form.address.value,
        addressZip: form.zip.value,
        addressCity: form.city.value
    };
}

function addressAutoComplete() {
    var placesAutocomplete = places({
        appId: 'pl9H5MQZCSC6',
        apiKey: 'ee11756711dbc7e6d011b9bc6e8bf981',
        container: document.getElementById('address'),
        countries: ['fr'],
        language: 'fr',

        templates: {
            value: function (suggestion) {
                return suggestion.name;
            }
        }
    }).configure({
        type: 'address'
    });
    placesAutocomplete.on('change', function resultSelected(e) {
        document.getElementById('city').value = e.suggestion.city || '';
        document.getElementById('zip').value = e.suggestion.postcode || '';
    });
}

function onBookingSuccess(form) {
    $.ajax('https://73k05.xyz/booking/new',{
        data: JSON.stringify(getParams(form)),
        contentType: 'application/json',
        type: 'POST',
        success: onBookingAddSuccess
    });
}

function onBookingAddSuccess() {
    console.log("Added to BOoked _o/")
}