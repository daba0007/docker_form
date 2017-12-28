//////////////////////容器从源拉取按钮///////////////////////
$('#image_pull').click(function() {
  var image,tag,reponame
  var t = $('#image_pull_form').serializeArray();
  $.each(t, function () {
      if (this.name=="image"){
          image=this.value;
      }
      if (this.name=="tag"){
          tag=this.value;
      }if (this.name=="reponame"){
          reponame=this.value;
      }
  });
  $.ajax({
        type: 'POST',
        data: {
            'image':image,
            'tag':tag,
            'reponame':reponame
        },
        url: "/docker_pull_image",
        async: false,
        success:function(data){
            alert(data["message"]);
        }
  });
  $(location).attr('href', '/image');
});

//////////////////////删除镜像///////////////////////
$("#image_btn_delete").click(function(){                                  // 删除按钮
    var a= $("#image_table").bootstrapTable('getSelections');
    idlist=[];
    repositorylist=[];
    for(i=0;i<a.length;i++){
        idlist[i]=Object.values(a[i])[1];
        repositorylist[i]=Object.values(a[i])[2];
    }
    if(a.length<=0){
        alert("请选中一行");
    }else{
        var url="/image_del";
        $.ajax({
            dataType: "json",
            traditional:true,//这使json格式的字符不会被转码
            data: {"idlist":idlist,"repositorylist":repositorylist},
            type: "post",
            url: url,
            async: false,       // 设置同步，则会等待服务器返回结果再返回成功信息
            success : function (data) {
                alert(data['message']);
            },
        });
    }
    $(location).attr('href', '/image');
});

/////////////////////基于已有镜像的容器创建镜像//////////
$('#image_btn_commit').click(function() {
  var container,reponame,tag
  var t = $('#image_commit_form').serializeArray();
  $.each(t, function () {
      if (this.name=="container"){
          container=this.value;
      }
      if (this.name=="reponame"){
          reponame=this.value;
      }
      if (this.name=="tag"){
          tag=this.value;
      }
  });
  $.ajax({
        dataType: "json",
        traditional:true,//这使json格式的字符不会被转码
        type: 'POST',
        data: {
            'container':container,
            'reponame':reponame,
            'tag':tag
        },
        url: "/image_commit",
        async: false,
        success:function(data){
            alert(data["message"]);
        },
  });
  $(location).attr('href', '/image');
});

///////////////////将dockerfile保存为文件到file/dockerfile////////
$('#push_btn_dockerfile').click(function() {
    var reponame
    var t = $('#image_dockerfile_from').serializeArray();
    $.each(t, function () {
        if (this.name=="reponame"){
          reponame=this.value;
        }
    });
    var file = $('#dockerfilename').val();
    $.ajax({
        dataType: "json",
        traditional:true,//这使json格式的字符不会被转码
        type: 'POST',
        data: {
            'reponame':reponame,
            'file':file,
        },
        url: "/image_dockerfile",
        async: false,
        success : function (data) {
            alert(data['message']);
        }
    });
    $(location).attr('href', '/image');
});