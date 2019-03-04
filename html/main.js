document.getElementById("review-file").addEventListener("change", function(e) {
  pywebview.api.show_review(e.target.value);
});