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

/////////////////////获取主机镜像//////////////
$("#image_hostlist li").click(function(){
    ip=$(this).text().replace(/\s+/g, "");
    $("#imagehead").text("主机"+ip+"镜像信息");
    $.ajax({
        type: 'POST',
        data: {
            'ip':ip,
        },
        url: "/image_newtable",
        async: false,
        dataType:"json",
        success:function(data){
            $("#image_table").bootstrapTable('load',data);
            alert("更新到"+ip);
        }
  });
})
////////////////////获取主机容器////////////////
$("#container_hostlist li").click(function(){
    ip=$(this).text().replace(/\s+/g, "");
    $("#containerhead").text("主机"+ip+"容器信息");
    $.ajax({
        type: 'POST',
        data: {
            'ip':ip,
        },
        url: "/container_newtable",
        async: false,
        dataType:"json",
        success:function(data){
            alert(data);
            alert("更新到"+ip);
        }
  });
})