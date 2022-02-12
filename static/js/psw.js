var password = document.getElementById("password")
  , psw-repeat = document.getElementById("psw-repeat");

function validatePassword(){
  if(password.value != psw-repeat.value) {
    psw-repeat.setCustomValidity("Passwords Don't Match");
  } else {
    psw-repeat.setCustomValidity('');
  }
}

password.onchange = validatePassword;
psw-repeat.onkeyup= validatePassword;