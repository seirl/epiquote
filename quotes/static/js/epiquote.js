function fav(id) {
  $.ajax({url: '/' + id + '/favourite', type: 'post'});
  var q = document.getElementById("f" + id);
  q.innerHTML = (q.innerHTML == '&lt;3') ? '&lt;/3' : '&lt;3';
}

function vote(slug, direction) {
  $.ajax({url: '/' + slug + '/' + direction + 'vote/', type: 'post'})
    .done(function (data) {
      $("#s" + slug).text(data.score)
      $("#t" + slug).text(data.num_votes)

      var dp = $("#dp" + slug);
      var dm = $("#dm" + slug);

      // Reset classes
      dp.removeClass("fw-bold text-success text-secondary");
      dm.removeClass("fw-bold text-danger text-secondary");
      dp.addClass("text-secondary");
      dm.addClass("text-secondary");

      if (data.current_vote == +1) {
        dp.removeClass("text-secondary").addClass("fw-bold text-success");
      }
      if (data.current_vote == -1) {
        dm.removeClass("text-secondary").addClass("fw-bold text-danger");
      }
    });
}

function rimshot() {
  document.getElementById('sound').innerHTML =
    "<audio src='/static/rimshot.wav' autoplay='autoplay'></audio>";
}
