$(document).ready(function() {
    var panelBodies = $('.panel-body');
    for(i=0; i<panelBodies.length; i++) {
        var $panelBody = $(panelBodies[i]);
        var input = '{}';

        input = $panelBody.find('#errorGetData').val();
        if(input == '') {
            input = '{}';
        };
        try {
            input = evalToJSON(input);
        } catch(error) {
            input = {};
        };
        $panelBody.find('#errorGet').jsonViewer(input, {collapsed: true});

        input = $panelBody.find('#errorPostData').val();
        if(input == '') {
            input = '{}';
        };
        try {
            input = evalToJSON(input);
        } catch(error) {
            input = {};
        };
        $panelBody.find('#errorPost').jsonViewer(input, {collapsed: true});

        input = $panelBody.find('#errorCookiesData').val();
        if(input == '') {
            input = '{}';
        };
        try {
            input = evalToJSON(input);
        } catch(error) {
            input = {};
        };
        $panelBody.find('#errorCookies').jsonViewer(input, {collapsed: true});
        
        input = $panelBody.find('#errorBodyData').val();
        if(input == '') {
            input = '{}';
        };
        try {
            input = evalToJSON(input);
        } catch(error) {
            input = {};
        };
        $panelBody.find('#errorBody').jsonViewer(input, {collapsed: true});

        input = $panelBody.find('#errorMetaData').val();
        if(input == '') {
            input = '{}';
        };
        try {
            input = evalToJSON(input);
        } catch(error) {
            input = {};
        };
        $panelBody.find('#errorMeta').jsonViewer(input, {collapsed: true});
    };
});