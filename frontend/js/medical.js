const minimumDelayBook = 7;

(function () {
    'use strict';
    window.addEventListener('load', function () {
        populateSelect();
        initBookDatePickers();
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    preventEvents(event);
                }
                else if (form.checkValidity() === true) {
                    preventEvents(event);
                    disableBookButton(form);
                    sendBookMail();
                }
                form.classList.add('was-validated');
            }, false);
        });
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

// Email JS init
(function () {
    emailjs.init("user_okaI2d5BZr9wdrnselFor");
})();

// Email JS send mail
function sendBookMail() {
    var form = document.getElementById('booking-form');
    sendMail(form);
};

function sendMail(form) {
    if (form == undefined || !form.checkValidity()) {
        console.error("Error, email empty or wrong or medical rendez-vous already sent");
        return;
    };

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

    showProgressBar();

    emailjs.send('commissionmedicale', 'commissionmedicale_template', params)
    .then(function (response) {
        console.log('SUCCESS!', response.status, response.text);
        hideProgressBar();
        showSuccesMessage();

    }, function (error) {
        enableBookButton(form);
        console.log('FAILED...', error);
        hideProgressBar();
        showErrorMEssage();
    });
};

function disableBookButton(form) {
    form.bookButton.disabled = true;
    return true;
};

function enableBookButton(form) {
    form.bookButton.disabled = false;
    return false;
};

function preventEvents(event) {
    event.preventDefault();
    event.stopPropagation();
};

function showSuccesMessage() {
    let succesMesage = document.getElementById("success-message");
    setTimeout(function () { succesMesage.style.display = 'block'; }, 2000);
};

function showErrorMEssage() {
    let errorMessage = document.getElementById("error-message");
    setTimeout(function () { errorMessage.style.display = 'block'; }, 2000);

};

function showProgressBar() {
    var progressBar = document.getElementById("progressId");
    progressBar.hidden = false;
};

function hideProgressBar() {
    var progressBar = document.getElementById("progressId");
    setTimeout(function () { progressBar.hidden = true; }, 2000);
};