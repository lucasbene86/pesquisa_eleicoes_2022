var se = document.getElementById('se');
var min = 0;
var max = se.innerHTML;
var duracao = 3000; // 3 segundos

for (var i = min; i <= max; i++) {
  setTimeout(function(nr) {
    se.innerHTML = nr;
  }, i * duracao / max, i);
}