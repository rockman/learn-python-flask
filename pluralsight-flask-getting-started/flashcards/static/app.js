(function() {

    function getHint(index, fn) {
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState == XMLHttpRequest.DONE) {
                if (xmlhttp.status == 200) {
                    fn(xmlhttp.responseText);
                }
            }
        };
        xmlhttp.open('GET', '/api/hint/' + index.toString());
        xmlhttp.send();
    }

    function prepareLink(id, dataName) {
        var link = document.getElementById(id);
        if (link) {
            getHint(link.dataset[dataName], function(responseText) {
                link.title = responseText;
            });
        }
    }

    prepareLink('link-prev', 'prev');
    prepareLink('link-next', 'next');

})();
