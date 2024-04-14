function showCommentBox(replyButton) {
  const parent = replyButton.parentNode.parentNode
  const commentBox = parent.querySelector('.comment-box')
  if (commentBox.style.display === "none") {
    commentBox.style.display = "block";
  } else {
    commentBox.style.display = "none";
  }
  replyButton.style.display = "none";
}

/**
 * Hero Slider
 */
var swiper = new Swiper(".sliderFeaturedPosts", {
  spaceBetween: 0,
  speed: 500,
  centeredSlides: true,
  loop: true,
  slideToClickedSlide: true,
  autoplay: {
    delay: 3000,
    disableOnInteraction: false,
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
  navigation: {
    nextEl: ".custom-swiper-button-next",
    prevEl: ".custom-swiper-button-prev",
  },
});