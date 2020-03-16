(function () {
    'use strict';
    window.addEventListener('load', function () {
        populateSelect();
        // Fetch all the forms we want to apply custom Bootstrap validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function (form) {
            form.addEventListener('submit', function (event) {
                if (form.checkValidity() === false) {
                    console.log('not true');
                    preventEvents(event);
                }
                else if (form.checkValidity() === true) {
                    console.log('form is true');
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
    }

    else if (age > 18) {
        birthdateInput.setCustomValidity('');
        errorMessage.style.display = "none";
    }

    else if (age === 18) {
        // your algorithm is our concern compute the exact day of the year 
    }
}

// Email JS init
(function () {
    emailjs.init("user_okaI2d5BZr9wdrnselFor");
})();

// Email JS send mail
function sendBookMail() {
    var form = document.getElementById('booking-form');
    sendMail(form, $("#contact-check"));
}

function sendMail(form, checkbutton) {
    if (form == undefined || !form.checkValidity()) {
        console.error("Error, email empty or wrong or medical rendez-vous already sent");
        return;
    }

    var email = form.email.value
    var firstname = form.firstname.value
    var lastname = form.lastname.value
    var phone = form.phone.value
    var birthdate = form.bday.value

    // generate the contact number value
    var number = Math.random() * 100000 | 0;

    var params = {
        email: email,
        firstname: firstname,
        lastname: lastname,
        phone: phone,
        number: number,
        birthdate: birthdate
    };

    form.is_already_sent.value = 'true';
    console.log('anything');
    emailjs.send('commissionmedicale', 'commissionmedicale_template', params)
        .then(function (response) {
            console.log('SUCCESS!', response.status, response.text);
            checkbutton.removeClass("hide");
        }, function (error) {
            enableBookButton(form);
            console.log('FAILED...', error);
            form.is_already_sent.value = false;
        });
}

function disableBookButton(form) {
    form.bookButton.disabled = true;
    return true;
}

function enableBookButton() {
    form.bookButton.disabled = false;
    return false;
};

function preventEvents(event){
    event.preventDefault();
    event.stopPropagation();
};
