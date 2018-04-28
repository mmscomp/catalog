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

// indexing up
function next(){
 if (idx >= 4){
     idx = 4;
  search();
   $('#button2').attr('disabled', true);
}else{
   $('#button1').attr('disabled', false);
   $('#button2').attr('disabled', false);
    search();
    idx++;
}
}

//indexing down
function prev(){
if(idx <= 0){
   idx = 0;
   $('#button1').attr('disabled', true);
   
console.log('70 '+ idx);
   search();
}else{
   
   $('#button2').attr('disabled', false);
   $('#button1').attr('disabled', false);
   search();
   --idx;
}
}


// Search for a specified string.
function search() {
  var q = $('#search').attr('name');

  var x = document.getElementById("btn");
      x.style.display = "flex";
      x.style.justifyContent = "center";
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
//Search for the meaning of the word
function findMeaning() {
 $('#meaning1').empty();
var q = $('#meaning').val();
 var wordUrl = "http://api.datamuse.com/words?ml=" + q;
    $.ajax({
        url: wordUrl,
        dataType: "json",
        json: "callback",
        success: function(response) {
            var wordList = response;
            var len;
            if (wordList.length){
            len = wordList.length;
            }else{
            len=0;
            }
            if(wordList.length > 5){
               len = 5;
            }
            for (var i = 0; i < len; i++) {

                wordStr = wordList[i].word;
                console.log(169, wordStr);
                $('#meaning1').append('<li>' + wordStr + '</li>');
            };

      //       console.log("2 " + wordList);
      //      clearTimeout(wikiRequestTimeout);
        }
    });

}

