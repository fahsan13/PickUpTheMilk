$(window).bind('scroll', function () {
    if ($(window).scrollTop() > 30) {
        $('.menu').addClass('fixed');
    } else {
        $('.menu').removeClass('fixed');
    }
});
