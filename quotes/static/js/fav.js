function fav(id) {
  $.post('/' + id + '/favourite');
  var q = document.getElementById("f" + id);
  if (q.innerHTML == '&lt;3') {
    q.innerHTML = '&lt;/3';
  }
  else
  {
    q.innerHTML = '&lt;3';
  }
}
