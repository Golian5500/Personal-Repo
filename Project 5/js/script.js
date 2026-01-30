const instagramNavbarMenu = document.querySelector('.instagram-navbar-menu');
const menuClicked = document.querySelector('.menu-clicked');
const leftPartMenuClicked = document.querySelector('.left-part-menu-clicked');

instagramNavbarMenu.addEventListener('click', function (event) {
    event.preventDefault();
    if (menuClicked.style.display == 'flex') {
        menuClicked.style.display = 'none';
    } else {
        menuClicked.style.display = 'flex';
    }
});
leftPartMenuClicked.addEventListener('click', function (event) {
    menuClicked.style.display = 'none';
});