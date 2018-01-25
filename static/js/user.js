function changeCheckCode(ths){
    ths.src = ths.src + '?';
}

$('#submit').click(function () {
    var $msg = $('#error_msg');
    $msg.parent().addClass('hide');
    $.ajax({
        url: '/login',
        type: 'POST',
        data: $('#loginform').serialize(),
        dataType: 'JSON',
        success: function (arg) {
            if(arg.status){
                location.href = '/home'
            }else{
                $msg.parent().removeClass('hide');
                $msg.text(arg.message);
                var img = $('#check_code_img')[0];
                img.src = img.src + '?';
                $('#password,#check_code').val('');
            }
        }
    })
})
