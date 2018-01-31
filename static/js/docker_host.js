//////////////////////加入主机///////////////////////
$('#docker_hostinput').click(function() {
  var ip,user,password
  var t = $('#docker_host_form').serializeArray();
  $.each(t, function () {
      if (this.name=="docker_hostip"){
          ip=this.value;
      }
      if (this.name=="docker_hostuser"){
          user=this.value;
      }if (this.name=="docker_hostpassword"){
          password=this.value;
      }
  });
  $.ajax({
        type: 'POST',
        data: {
            'ip':ip,
            'user':user,
            'password':password
        },
        url: "/post_docker_hosts",
        async: false,
        success:function(data){
            alert(data["message"]);
        }
  });
  $(location).attr('href', '/host_in_docker');
});