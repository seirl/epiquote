function vote(slug, direction) {
    $.post('/' + slug + '/' + direction + 'vote/');
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
