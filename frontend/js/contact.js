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
          
function getTemplate () {
    return 'commissionmedicale_template';
}

function getParams (form) {
  var email = form.email.value;
  var firstname = form.firstname.value;
  var message = form.message.value;

    params = {
    email: email,
    firstname: firstname,
    message: message
  };
}
