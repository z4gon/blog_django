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