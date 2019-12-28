$(function() {
    $('#btn1').click(function() {
        $.ajax({
            url: '/LlamarEncenderL1',
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#btn2').click(function() {
        $.ajax({
            url: '/LlamarApagarL1',
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#btn3').click(function() {
        $.ajax({
            url: '/LlamarEncenderL2',
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#btn4').click(function() {
        $.ajax({
            url: '/LlamarApagarL2',
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#btn5').click(function() {
        $.ajax({
            url: '/LlamarEncenderL3',
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
    $('#btn6').click(function() {
        $.ajax({
            url: '/LlamarApagarL3',
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

