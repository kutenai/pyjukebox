/**
 * Created by kutenai on 7/2/15.
 */

function play_song(elem) {
    var url = $(elem).attr('playlink');
    $.ajax(url);
    return false;
}

