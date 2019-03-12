document.addEventListener("DOMContentLoaded", function (e) {
  let h = location.hash;
  if(h.substr(0, 4) == "#top"){
    window.scroll(0, parseInt(h.substring(4)));
  }
})
document.addEventListener("scroll", function (e) {
  window.parent.postMessage(document.documentElement.scrollTop, "*");
})