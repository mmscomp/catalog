/ After the API loads, call a function to enable the search box.
 var sub = $('#sub').text();
console.log("1 " + sub);
var $wiki = $('#wiki');
console.log("2 " + $wiki);
console.log("3 " + $('#search').attr('name'));
//$wiki.text("");
$wiki.dblclick (function(){
//function loadWiki(){
var wikiUrl = 'http://en.wikipedia.org/w/api.php?action=opensearch&search=' + sub + '&format=json&callback=wikiCallback';
   var wikiRequestTimeout = setTimeout(function() {
        $wiki.text("failed to get wikipedia resources");
    }, 10000);

    $.ajax({
        url: wikiUrl,
        dataType: "jsonp",
        jsonp: "callback",
        success: function(response) {
            var articleList = response[1];
            var len;
            if (articleList.length){
            len = articleList.length;
            }else{
            len=0;
            }
            if(articleList.length > 3){
               len = 3;
            }
            for (var i = 0; i < len; i++) {

                articleStr = articleList[i];
                var url = 'http://en.wikipedia.org/wiki/' + articleStr;
                $wiki.append('<li><a href="' + url + '" target="_blank">' + articleStr + '</a></li>');
            };

             console.log("2 " + articleList);
            clearTimeout(wikiRequestTimeout);
        }
    });
});


function handleAPILoaded() {
  $('#search').attr('disabled', false);
}

// Search for a specified string.
function search() {
  var q = $('#search').attr('name');
  var request = gapi.client.youtube.search.list({
    q: q,
    part: 'snippet'
  });

  request.execute(function(response) {
    var str = JSON.stringify(response.result);
    console.log(response.result.items[0].id.videoId);//.snippet.thumbnails.medium);
    var id = response.result.items[0].id.videoId;
    var src = '<iframe src=' + '"https://youtube.com/embed/' + id +'" width=200 height=100 </ifram>';
    console.log(src);
   $('#search-container').html('<pre>' + id + '</pre>');
   $('#search-container').html('<iframe src=' + '"https://youtube.com/embed/' + id +'" width=600 height=400 </ifram>');
  });
}

