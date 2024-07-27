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
                    '<div class="ip-info"><span class="ip-label">内网 IPv4：</span>' + response.internal_ipv4 + '</div>' +
                    '<div class="ip-info"><span class="ip-label">内网 IPv6：</span>' + response.internal_ipv6 + '</div>' +
                    '<div class="ip-info"><span class="ip-label">公网 IPv4：</span>' + response.public_ipv4 + '</div>' +
                    '<div class="ip-info"><span class="ip-label">公网 IPv6：</span>' + response.public_ipv6 + '</div>'
                );
            },
            error: function() {
                $('#result').html('<p>发生错误，请重试。</p>');
            }
        });
    });
});
