let title = document.querySelector("h1");

title.addEventListener("click", newTitle);
function newTitle() {
  title.innerHTML = "Nouveau titre";
  title.style.backgroundColor = "yellow";
}
