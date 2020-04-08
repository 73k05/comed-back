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
  return "contact_template";
}

function getParams(form) {
  var email = form.email.value;
  var firstname = form.firstname.value;

  var params = {
    email: email,
    firstname: firstname,
  };
}
