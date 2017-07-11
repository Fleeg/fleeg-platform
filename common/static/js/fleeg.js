// profile menu
function highlightProfileMenu() {
    name = window.location.pathname.split('/').pop();
    active = '#'+ name + '-menu';
    $('.fmenu-profile li').removeClass('active');
    if(name && name !== "") {
        $(active).addClass('active');
    }
    else {
        $('#profile-menu').addClass('active');
    }
}
