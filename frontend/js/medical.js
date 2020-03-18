const minimumDelayBook = 7;

(function () {
    'use strict';
    window.addEventListener('load', function () {
        populateSelect();
        initBookDatePicker();
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                submitBday();
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

// calculate age
function submitBday() {
    let errorMessage = document.getElementById('age-error-message');
    let birthdateInput = document.getElementById('birthday-input');

    let today = new Date();
    let dateTodayYear = today.getFullYear();
    let Bdate = birthdateInput.value;
    let Bday = new Date(Bdate);
    let yearOfBirth = Bday.getFullYear();
    let age = (dateTodayYear - yearOfBirth);

    if (age < 18) {
        errorMessage.style.display = "block";
        birthdateInput.setCustomValidity('useless error message');
        return false;
    }

    else if (age > 18) {
        birthdateInput.setCustomValidity('');
        errorMessage.style.display = "none";
        return true;
    }

    else if (age === 18) {
        return true;
        // your algorithm is our concern compute the exact day of the year 
    }
};

// Email JS init
(function () {
    emailjs.init("user_okaI2d5BZr9wdrnselFor");
})();

// Email JS send mail
function sendBookMail() {
    var form = document.getElementById('booking-form');
    sendMail(form, $("#contact-check"));
};

function sendMail(form, checkbutton) {
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

// Display Booking Date

function initBookDatePicker() {
    let displayBookingInput = document.getElementById('bookingDate-input');
    let nextWeekDate = new Date();
    // Calculating the actual day date + 6 days ahead
    nextWeekDate.setDate(nextWeekDate.getDate() + minimumDelayBook);
    displayBookingInput.min = nextWeekDate.getFullYear().toString() + '-' + (nextWeekDate.getMonth() + 1).toString().padStart(2, 0)
        + '-' + nextWeekDate.getDate().toString().padStart(2, 0);
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