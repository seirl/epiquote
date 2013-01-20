function fav(id) {
  $.post('/'+id+'/favourite', {HTTP_X_REQUESTED:'XMLHttpRequest'});
  var q = document.getElementById("f" + id);
  if (q.innerHTML == '&lt;3') {
    q.innerHTML = '&lt;/3';
  }
  else
  {
    q.innerHTML = '&lt;3';
  }
}
