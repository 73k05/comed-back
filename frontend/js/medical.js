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
                    event.preventDefault();
                    event.stopPropagation();
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
function sendMail(form, checkbutton) {
    if (form == undefined || !form.checkValidity() || form.is_already_sent.value == 'true') {
        console.error("Error, email empty or wrong or medical rendez-vous already sent");
        return;
    }

    var email = form.email.value
    // generate the contact number value
    var number = Math.random() * 100000 | 0;
    var name = email.substring(0, email.indexOf('@'));

    var params = {
        email: email,
        firstname: firstname,
        lastname: lastname,
        phone: phone,
        number: number,
        bday: bday
    };

    form.is_already_sent.value = 'true';
    emailjs.send('inkos', 'inkos_template', params)
        .then(function (response) {
            console.log('SUCCESS!', response.status, response.text);
            checkbutton.removeClass("hide");
        }, function (error) {
            console.log('FAILED...', error);
            form.is_already_sent.value = false;
        });
}
