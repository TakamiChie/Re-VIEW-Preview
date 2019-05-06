document.getElementById("review-file").addEventListener("change", function(e) {
  pywebview.api.show_review(e.target.value);
});

document.getElementById("refresh_view").addEventListener("click", function(e) {
  pywebview.api.show_review();
})

document.getElementById("directory_open").addEventListener("click", function(e) {
  pywebview.api.directory_open();
})

var pos = 0;

window.addEventListener("message", function (e) {
  pos = e.data;
})