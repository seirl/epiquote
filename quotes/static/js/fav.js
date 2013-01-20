function fav(id) {
  $.post('/'+id+'/favourite', {HTTP_X_REQUESTED:'XMLHttpRequest'});
  var q = document.getElementById("f" + id);
  if (q.innerHTML == 'Supprimer des favoris') {
    q.innerHTML = 'Ajouter en favori';
  }
  else
  {
    q.innerHTML = 'Supprimer des favoris';
  }
}
