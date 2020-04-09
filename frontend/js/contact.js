(function () {
    "use strict";
    window.addEventListener(
        "load",
        function () {
            initEventListener();
        },
        false
    );
})();

function getTemplate() {
    return 'commissionmedicale_template';
}

function getParams(form) {
    return {
        email: form.email.value,
        firstname: form.firstname.value,
        message: form.message.value
    };
}
