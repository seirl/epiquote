function fav(id) {
  $.ajax({url: '/' + id + '/favourite', type: 'post'});
  var q = document.getElementById("f" + id);
  if (q.innerHTML == '&lt;3') {
    q.innerHTML = '&lt;/3';
  }
  else
  {
    q.innerHTML = '&lt;3';
  }
}

function vote(slug, direction) {
  $.ajax({url: '/' + slug + '/' + direction + 'vote/', type: 'post'});
  var s = document.getElementById("s" + slug),
    t = document.getElementById("t" + slug),
    d = document.getElementById("d" + slug),
    ns = parseInt(s.innerHTML, 10),
    nt = parseInt(t.innerHTML, 10);

  s.innerHTML = (ns + 1) + '';
  if (direction == 'up') {
    s.innerHTML = (ns + 1) + '';
    t.innerHTML = (nt + 1) + '';
    d.innerHTML = '';
  }
  else if (direction == 'down') {
    s.innerHTML = (ns - 1) + '';
    t.innerHTML = (nt + 1) + '';
    d.innerHTML = '';
  }
}

function rimshot() {
  document.getElementById('sound').innerHTML =
    "<audio src='/static/rimshot.wav' autoplay='autoplay'></audio>";
}
