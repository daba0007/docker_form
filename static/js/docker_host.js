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
        dataType: "json",
        async: false,
        success:function(data){
            alert(data['message']);
        }
  });
  $(location).attr('href', '/host_in_docker');
});

/////////////////////删除主机////////////////////
$('#docker_host_btn_delete').click(function() {
    var a= $("#docker_host_table").bootstrapTable('getSelections');
    idlist=[];
    for(i=0;i< a.length ;i++){
        idlist[i]=Object.values(a[i])[1];
    }
    if(a.length<=0){
        alert("请选中一行");
    }else{
        var url="/delte_docker_host";
        $.ajax({
            dataType: "json",
            traditional:true,       //这使json格式的字符不会被转码
            data: {"idlist":idlist},
            type: "post",
            url: url,
            async: false,           // 设置同步，则会等待服务器返回结果再返回成功信息
            success : function (data) {
                alert(data['message']);
            },
        });
    }
  $(location).attr('href', '/host_in_docker');
});

/////////////////////image页面获取主机镜像//////////////
$("#image_hostlist li").click(function(){
    ip=$(this).text().replace(/\s+/g, "");
    $("#imagehead").text(ip);
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
        }
  });
})

/////////////////////image_add页面获取主机镜像//////////////
$("#image_all_list li").click(function(){
    ip=$(this).text().replace(/\s+/g, "");
    $("#image_add_head").text(ip);
})

////////////////////container页面获取主机容器////////////////
$("#container_hostlist li").click(function(){
    ip=$(this).text().replace(/\s+/g, "");
    $("#containerhead").text(ip);
    $.ajax({
        type: 'POST',
        data: {
            'ip':ip,
        },
        url: "/container_newtable",
        async: false,
        dataType:"json",
        success:function(data){
            $("#container_table").bootstrapTable('load',data);
        }
  });
})


