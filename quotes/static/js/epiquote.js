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

function vote(slug, direction, was=0) {
  $.ajax({url: '/' + slug + '/' + direction + 'vote/', type: 'post'});
  var s = document.getElementById("s" + slug),
    t = document.getElementById("t" + slug),
    d = document.getElementById("d" + slug),
    ns = parseInt(s.innerHTML, 10),
    nt = parseInt(t.innerHTML, 10);

  if (direction == 'up') {
    s.innerHTML = (ns + (was ? 2 : 1)) + '';
    t.innerHTML = (nt + (was ? 0 : 1)) + '';
    d1.innerHTML = "<a href=\"javascript:void(0)\" onclick=\"vote('1', 'clear', 1);\"><b>(+)</b></a><a href=\"javascript:void(0)\" onclick=\"vote('1', 'down', 1);\">(-)</a>"
  }
  else if (direction == 'down') {
    s.innerHTML = (ns - (was ? 2 : 1)) + '';
    t.innerHTML = (nt + (was ? 0 : 1)) + '';
    d.innerHTML = "<a href=\"javascript:void(0)\" onclick=\"vote('1', 'up', -1);\">(+)</a><a href=\"javascript:void(0)\" onclick=\"vote('1', 'clear', -1);\"><b>(-)</b></a>"
  }
  else if (direction == 'clear'){
    s.innerHTML = (ns - was) + '';
    t.innerHTML = (nt - 1) + '';
    d.innerHTML = "<a href=\"javascript:void(0)\" onclick=\"vote('1', 'up');\">(+)</a><a href=\"javascript:void(0)\" onclick=\"vote('1', 'down');\">(-)</a>"
  }
}

function rimshot() {
  document.getElementById('sound').innerHTML =
    "<audio src='/static/rimshot.wav' autoplay='autoplay'></audio>";
}
