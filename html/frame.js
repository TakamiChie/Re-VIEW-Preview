document.addEventListener("DOMContentLoaded", function (e) {
  let h = location.hash;
  if(h.substr(0, 4) == "#top"){
    window.scroll(0, parseInt(h.substring(4)));
  }

  // Create TOC.
  let toc = document.createElement("nav")
  toc.id = "toc"
  let header = document.createElement("div")
  header.id = "TOCHeader";
  header.textContent = "TOC";
  header.addEventListener("click", function (e) {
    var b = document.getElementById("TOCBody");
    b.style.display = b.style.display == "none" ? "block" : "none";
  });
  let ul = document.createElement("ul");
  ul.id = "TOCBody";
  {
    let nodes = Array.prototype.slice.call(document.querySelectorAll("h1,h2,h3,h4,h5,h6"),0)
    nodes.forEach(function(e){
      let hl = parseInt(e.tagName.substr(1, 1))
      let li = document.createElement("li");
      li.style.marginLeft = (hl - 1) + "ex";
      let a = document.createElement("a");
      a.href = "#" + e.querySelector("a").id;
      if(e.querySelector("a").id.indexOf("column") != -1){
        a.textContent = "[c] ";
      }
      a.textContent += e.textContent;
      li.appendChild(a);
      ul.appendChild(li);
    });
  }
  toc.appendChild(header);
  toc.appendChild(ul);
  document.body.appendChild(toc);
})
document.addEventListener("scroll", function (e) {
  window.parent.postMessage(document.documentElement.scrollTop, "*");
})