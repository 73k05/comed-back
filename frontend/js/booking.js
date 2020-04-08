(function () {
    'use strict';
    window.addEventListener('load', function () {
        initEventListener ();
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
        onSelect: function(date) {
        },
        format: "dd/mm/yyyy",
        startDate: nextWeekDate,
        firstDay: 1,
    });

    // Calculating the actual day date - 18 years behind
    let minBirthDate = new Date()
    minBirthDate.setFullYear(new Date().getFullYear() - 18);    
    $("#birthDatePicker").datepicker({
        onSelect: function(date) {
        },
        format: "dd/mm/yyyy",
        endDate: minBirthDate,
        firstDay: 1,
    });
};

function getTemplate(){
    return 'commissionmedicale_template';
}

function getParams (form) {
    var email = form.email.value
    var firstname = form.firstname.value
    var lastname = form.lastname.value
    var phone = form.phone.value
    var birthdate = form.bday.value
    var birthname = form.birthname.value
    var region = form.selectregion.value
    var selectcase = form.selectcase.value
    var bookingdate = form.bookingdate.value

    // generate the contact number value
    var number = Math.random() * 100000 | 0;

    var params = {
        email: email,
        firstname: firstname,
        lastname: lastname,
        phone: phone,
        number: number,
        birthdate: birthdate,
        birthname: birthname,
        region: region,
        typevisit: selectcase,
        datebooking: bookingdate 
    };
    return params;
}