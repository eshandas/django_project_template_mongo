$(document).ready(function() {
    var panelBodies = $('.panel-body');
    for(i=0; i<panelBodies.length; i++) {
        var $panelBody = $(panelBodies[i]);
        try {
            try {
                var input = eval('(' + $panelBody.find('#logRequestDataData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logRequestData').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#logRequestHeadersData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logRequestHeaders').jsonViewer(input, {collapsed: true});

            try {
                var input = eval('(' + $panelBody.find('#logResponseTextData').val() + ')');
            } catch(err) {
                var input = {};
            }
            $panelBody.find('#logResponseText').jsonViewer(input, {collapsed: true});

        }
        catch (log) {
            alert("Cannot eval JSON: " + log);
        }
    };

    $('#btnDeleteLogs').click(function() {
        var r = confirm('Are you sure you want to delete all request logs? It will irreparably delete all the request logs.');
        if(r == true) {
            $('#deleteLogs').submit();
        }
    });
});