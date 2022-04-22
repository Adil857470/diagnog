let border = '1px solid red';

function validation() {
    let fn = document.getElementById('fname'),
        ln = document.getElementById('lname'),
        mail = document.getElementById('mail'),
        num = document.getElementById('num'),
        pass = document.getElementById('pass');
    if (fn.value == " " || fn.value == '') {
        fn.style.border = border;
        return false;
    } else if (fn.value.length < 3 || fn.value.length > 25) {
        fn.style.border = border;
        return false;
    }
    if (ln.value == " " || ln.value == '') {
        ln.style.border = border;
        return false;
    } else if (ln.value.length < 3 || ln.value.length > 25) {
        ln.style.border = border;
        return false;
    }
    if (num.value == '' || num.value == ' ') {
        num.style.border = border;
        return false;
    } else if (num.value.length < 10) {
        num.style.border = border;
        return false;
    }
    if (mail.value == " " || mail.value == '') {
        mail.style.border = border;
        return false;
    } else if (mail.length < 13 || mail.length > 40) {
        mail.style.border = border;
        return false;
    }
}

function val() {
    let num = document.getElementById('num');
    if (isNaN(num.value)) {
        num.style.border = border;
        return false;
    } else if (!isNaN(num.value)) {
        return true;
    }
}