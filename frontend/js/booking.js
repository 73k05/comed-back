(function () {
    'use strict';
    window.addEventListener('load', function () {
        initEventListener();
        populateSelect();
        initBookDatePickers();

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
        bookingdate: form.bookingdate.value
    };
}