(function () {
    'use strict';
    window.addEventListener('load', function () {
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


