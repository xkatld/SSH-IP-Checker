$(document).ready(function() {
    $('#ssh-form').submit(function(e) {
        e.preventDefault();
        $('#result').html('<p>正在查询，请稍候...</p>');
        $('#error-message').html('');
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
                console.log("Received response:", response);
                if (response.internal_ipv4 || response.internal_ipv6 || response.public_ipv4 || response.public_ipv6) {
                    $('#result').html(
                        '<div class="ip-info"><span class="ip-label">内网 IPv4：</span>' + (response.internal_ipv4 || 'N/A') + '</div>' +
                        '<div class="ip-info"><span class="ip-label">内网 IPv6：</span>' + (response.internal_ipv6 || 'N/A') + '</div>' +
                        '<div class="ip-info"><span class="ip-label">公网 IPv4：</span>' + (response.public_ipv4 || 'N/A') + '</div>' +
                        '<div class="ip-info"><span class="ip-label">公网 IPv6：</span>' + (response.public_ipv6 || 'N/A') + '</div>'
                    );
                } else {
                    $('#result').html('<p>无法获取 IP 地址，请检查输入信息是否正确。</p>');
                }
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error("AJAX error:", textStatus, errorThrown);
                $('#error-message').html('发生错误，请重试。错误信息: ' + textStatus);
                $('#result').html('');
            }
        });
    });
});
