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
  $.ajax({url: '/' + slug + '/' + direction + 'vote/', type: 'post'})
    .done(function (data) {
      $("#s" + slug).text(data.score)
      $("#t" + slug).text(data.num_votes)

      var dp = $("#dp" + slug);
      var dm = $("#dm" + slug);
      dp.removeClass("voteon");
      dm.removeClass("voteon");
      if (data.current_vote == +1)
        dp.addClass("voteon");
      if (data.current_vote == -1)
        dm.addClass("voteon");
    });
  return false;
}

function rimshot() {
  document.getElementById('sound').innerHTML =
    "<audio src='/static/rimshot.wav' autoplay='autoplay'></audio>";
}
