// Javascript

let toggle = document.getElementById('toggle'); /** below function is used to toggle the navlinks from viwport below 1200px */
toggle.onclick = function() {
    toggle.classList.toggle('active');
    document.querySelector('.cover').classList.add('active');
    document.querySelector('.navlnks').classList.add('active');
}

let search = document.querySelector('.srch');
search.onclick = function() {
    search.classList.toggle('active');
    document.querySelector('.search').classList.toggle('active');
}
let showCart = () => document.querySelector('.cart').classList.add('active');

let closeCart = () => document.querySelector('.cart').classList.remove('active');

let closeNavbar = () => {
    document.querySelector('.toggle').classList.remove('active');
    document.querySelector('.navlnks').classList.remove('active');
    document.querySelector('.cover').classList.remove('active');
}
let l = document.querySelectorAll('.link');
for (let i = 0; i < l.length; i++) {
    l[i].onclick = function() {
        let j = 0;
        while (j < l.length) {
            l[j++].className = 'link';
        }
        l[i].classList.toggle('active');
    }
}

const cat = () => {
    let a = document.querySelectorAll('#submenu a').length;
    // console.log(a);
    if (a < 10) {
        document.getElementById('submenu').style.height = 380;
    } else {
        document.getElementById('submenu').style.height = 'auto';
    }
}

let mnu = document.querySelector('.submnu');
mnu.onclick = function() {
    mnu.classList.toggle('active')
};

if (screen.availWidth >= 300) {
    let navbar = document.querySelector(".navbar1");
    window.addEventListener('scroll', () => {
        window.scrollY > 450 ? navbar.classList.add("sticky") : navbar.classList.remove("sticky");
        console.log(window.scrollY);
    })
}

// jquery


$(".cl li").hover(function() {
    var isHovered = $(this).is(":hover");
    if (isHovered) {
        $('.drop').stop().fadeIn(200);
    } else {
        $('.drop').stop().fadeOut(200);
    }
});

$(function() {
    $("#item").click(function() {
        $("#submenu").slideToggle(300);
    });
});