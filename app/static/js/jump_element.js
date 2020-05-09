var animation = anime({
    targets: '.jumping_element',
    translateY: 500,
    direction: 'alternate',
    loop: true,
    easing: 'easeInOutQuad',
    autoplay: true
});

function loop(t) {
    animation.tick(t);
    customRAF = requestAnimationFrame(loop);
}

requestAnimationFrame(loop);