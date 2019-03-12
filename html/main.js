document.getElementById("review-file").addEventListener("change", function(e) {
  pywebview.api.show_review(e.target.value);
});

document.getElementById("refresh_view").addEventListener("click", function(e) {
  pywebview.api.show_review();
})

var pos = 0;

window.addEventListener("message", function (e) {
  pos = e.data;
})