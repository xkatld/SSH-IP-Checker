$(document).ready(function() {
    $('#ssh-form').submit(function(e) {
        e.preventDefault();
        $('#result').html('<p>正在查询，请稍候...</p>');
        $.ajax({
            url: '/',
            method: 'POST',
            data: {
                hostname: $('#hostname').val(),
                port: $('#port').val(),
                username: $('#username').val(),
                password: $('#password').val()
            },
            success: function(response) {
                $('#result').html(
                    '<div class="ip-info"><span class="ip-label">内网 IP：</span>' + response.internal_ip + '</div>' +
                    '<div class="ip-info"><span class="ip-label">公网 IP：</span>' + response.public_ip + '</div>'
                );
            },
            error: function() {
                $('#result').html('<p>发生错误，请重试。</p>');
            }
        });
    });
});
