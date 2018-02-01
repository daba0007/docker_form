/////////////////容器按钮操作////////////////////////////
////////////////创建容器按钮//////////////
$('#container_pull').click(function() {
    var image,command,tag,reponame,con_name,check_d,check_volume,check_port,check_link,check_volume_from,volume_from_select //这个数据卷容器暂时用数，添加方式不确定。
    var ip=$("#container_add_head").text()
    var volume_permission=[]
    var alias_name=[]
    var host_name=[]
    var volume_local_list=[]
    var volume_container_list=[]
    var port_local_list=[]
    var port_container_list=[]
    var d={};
    var t = $('#container_pull_form').serializeArray();
    volume_local_num=0
    volume_container_num=0
    port_local_num=0
    port_container_num=0
    volume_permission_num=0
    alias_num=0
    host_num=0
    $.each(t, function () {
        if (this.name=="container"){                // 镜像名
          image=this.value;
        }
        if (this.name=="reponame"){                 // 镜像源
          reponame=this.value;
        }
        if (this.name=="tag"){                      // 版本号
          tag=this.value;
        }
        if (this.name=="command"){                  // 命令
          command=this.value;
        }
        if (this.name=="con_name"){                 // 容器名
          con_name=this.value;
        }
        if (this.name=="check_d"){                  // 是否后台运行
          check_d=this.value;
        }
        if (this.name=="check_volume"){             // 是否增加数据卷
          check_volume=this.value;
        }
        if (this.name=="volume_local_name"){        //数据卷本地位置
          volume_local_list[volume_local_num]=this.value;
          volume_local_num++;
        }
        if (this.name=="volume_container_name"){    // 数据卷容器位置
          volume_container_list[volume_container_num]=this.value;
          volume_container_num++;
        }
        if (this.name=="volume_permission"){    // 数据卷容器位置
          volume_permission[volume_permission_num]=this.value;
          volume_permission_num++;
        }
        if (this.name=="check_port"){             // 是否增加端口映射
          check_port=this.value;
        }
        if (this.name=="port_local_name"){          // 端口本地位置
          port_local_list[port_local_num]=this.value;
          port_local_num++;
        }
        if (this.name=="port_container_name"){      //端口容器位置
          port_container_list[port_container_num]=this.value;
          port_container_num++;
        }
        if(this.name=="check_link"){                 // 是否网络连接
            check_link=this.value;
        }
        if(this.name=="alias_name"){                 // 别名
            alias_name[alias_num]=this.value;
            alias_num++;
        }
        if(this.name=="host_name"){                 // 容器中名
            host_name[host_num]=this.value;
            host_num++;
        }
        if(this.name=="check_volume_from") {          //是否连接数据卷
            check_volume_from=this.value;
        }
        if(this.name=="volume_from_select"){           //数据卷容器
            volume_from_select=this.value;
        }
    });
    $.ajax({
        type: 'POST',
        url: "/docker_create_container",
        dataType: "json",
        data: {
            'ip':ip,
            'container':image,
            'reponame':reponame,
            'tag':tag,
            'command':command,
            'name':con_name,
            'check_d':check_d,
            'check_volume':check_volume,
            'volume_local_list':volume_local_list,
            'volume_container_list':volume_container_list,
            'volume_permission':volume_permission,
            'check_port':check_port,
            'port_local_list':port_local_list,
            'port_container_list':port_container_list,
            'check_link':check_link,
            'alias_name':alias_name,
            'host_name':host_name,
            'check_volume_from':check_volume_from,
            'volume_from_select':volume_from_select
        },
        async: false,
        success:function(data){
            alert(data['message']);
        }
    });
    $(location).attr('href', '/container');
});
////////////////删除容器按钮///////////
$("#con_btn_delete").click(function(){                                  // 删除按钮
    var a= $("#container_table").bootstrapTable('getSelections');
    var ip=$("#container_add_head").text()
    idlist=[];
    statuslist=[]
    for(i=0;i<a.length;i++){
        idlist[i]=Object.values(a[i])[1];
        statuslist[i]=Object.values(a[i])[5];
    }
    if(a.length<=0){
        alert("请选中一行");
    }else{
        var url="/container_rm";
        $.ajax({
            dataType: "json",
            traditional:true,//这使json格式的字符不会被转码
            data: {"idlist":idlist,"statuslist":statuslist,"ip":ip},
            type: "post",
            url: url,
            async: false,       // 设置同步，则会等待服务器返回结果再返回成功信息
            success : function (data) {
                alert(data['message']);
            },
        });
    }
    $(location).attr('href', '/container');
});
///////////////容器操作/////////////运行，停止，暂停，继续
///////////////设置按钮/////////////////
function add_container_operate(value,row,index){                //按钮
    return[
        '<button id="con_start_btn" type="button" class="btn btn-success btn-xs" style="display: table"><span class="glyphicon glyphicon-play" ></span>运行</button>',
        '<button id="con_stop_btn" type="button" class="btn btn-danger btn-xs" style="display: table"><span class="glyphicon glyphicon-stop" ></span>停止</button>',
        '<button id="con_pause_btn" type="button" class="btn btn-warning btn-xs" style="display: table"><span class="glyphicon glyphicon-pause" ></span>暂停</button>',
        '<button id="con_unpause_btn" type="button" class="btn btn-info btn-xs" style="display: table"><span class="glyphicon glyphicon-repeat" ></span>继续</button>'
    ].join("")
}
///////////////设置按钮操作///////////
window.container_operate ={                                         //按钮操作
    "click #con_start_btn":function(e,value,row,index){        //开始按钮
        var url="/container_start";
        var ip=$("#container_add_head").text();
        $.ajax({
            dataType: "json",
            traditional:true,//这使json格式的字符不会被转码
            data: {
                "id":row.id,
                "status":row.status,
                "ip":ip
            },
            type: 'POST',
            url: url,
            async: false,       // 设置同步，则会等待服务器返回结果再返回成功信息
            success : function (data) {
                alert(data['message']);
            }
        });
        $(location).attr('href', '/container');
    },
    "click #con_stop_btn":function(e,value,row,index){         //退出按钮
        var url="/container_stop";
        var ip=$("#container_add_head").text();
        $.ajax({
            dataType: "json",
            traditional:true,//这使json格式的字符不会被转码
            data: {
                "id":row.id,
                "status":row.status,
                "ip":ip
            },
            type: 'POST',
            url: url,
            async: false,       // 设置同步，则会等待服务器返回结果再返回成功信息
            success : function (data) {
                alert(data["message"]);
            }
        });
        $(location).attr('href', '/container');
    },
    "click #con_pause_btn":function(e,value,row,index){        //暂停按钮
        var url="/container_pause";
        var ip=$("#container_add_head").text();
        $.ajax({
            dataType: "json",
            traditional:true,//这使json格式的字符不会被转码
            data: {
                "id":row.id,
                "status":row.status,
                "ip":ip
            },
            type: 'POST',
            url: url,
            async: false,       // 设置同步，则会等待服务器返回结果再返回成功信息
            success : function (data) {
                alert(data["message"]);
            }
        });
        $(location).attr('href', '/container');
    },
    "click #con_unpause_btn":function(e,value,row,index){      //继续按钮
        var url="/container_unpause";
        var ip=$("#container_add_head").text()
        $.ajax({
            dataType: "json",
            traditional:true,//这使json格式的字符不会被转码
            data: {
                "id":row.id,
                "status":row.status,
                "ip":ip
            },
            type: 'POST',
            url: url,
            async: false,       // 设置同步，则会等待服务器返回结果再返回成功信息
            success : function (data) {
                alert(data["message"]);
            }
        });
        $(location).attr('href', '/container');
    },
}
///////////////增加元素///////////
///////////////增加容器卷///////////////
///////////////判断是否增加容器卷///////////////
$("#check_volume").click(function(){
    $("#volume_local_name").show()
    $("#volume_con_name").show()
    $("#check_volume").hide()
    $("#volume_add").show()
    $("#volume_permission").show()
});
///////////////增加容器卷/////////////////////
$('#volume_add').click(function() {
    $("#port_form").before(" <div class='form-group'>" +
        "                           <label class='col-sm-2 control-label'>数据卷</label>" +
        "                               <div class='col-sm-4'>" +
        "                                   <input type='text' class='form-control' name='volume_local_name' placeholder='本地:/www/static(选填)'>" +
        "                               </div>" +
        "                               <div class='col-sm-4'>" +
        "                                   <input type='text' class='form-control' name='volume_container_name' placeholder='容器:/web/static(选填)'>" +
        "                               </div>" +
        "                               <div class='col-sm-2'>"+
        "                                   <select class='form-control' id='volume_permission' name='volume_permission' >"+
        "                                       <option>rw</option><option>ro</option>"+
        "                                   </select>"+
        "                               </div>"+
        "                      </div>" );
});
///////////////增加端口映射////////////////////////
///////////////判断是否增加端口映射/////////////////
$("#check_port").click(function(){
    $("#port_local_name").show()
    $("#port_con_name").show()
    $("#check_port").hide()
    $("#port_add").show()

});
///////////////判断增加多少端口映射//////////////
$('#port_add').click(function() {
    $("#link_form").before(" <div class='form-group'>" +
        "                           <label class='col-sm-2 control-label'>端口映射</label>" +
        "                               <div class='col-sm-5'>" +
        "                                   <input type='text' class='form-control' name='port_local_name' placeholder='本地端口:80(选填)'>" +
        "                               </div>" +
        "                               <div class='col-sm-5'>" +
        "                                   <input type='text' class='form-control' name='port_container_name' placeholder='容器端口:8000(选填)'>" +
        "                               </div>" +
        "                           </div>" );
});
//////////////增加网络连接//////////////
///////////////判断是否增加网络连接///////////
$("#check_link").click(function(){
    $("#alias_name").show()
    $("#host_name").show()
    $("#check_link").hide()
    $("#link_add").show()
});
///////////////判断增加多少网络连接//////////
$('#link_add').click(function() {
    $("#volume_from_form").before(" <div class='form-group'>" +
        "                           <label class='col-sm-2 control-label'>连接其他容器</label>" +
        "                               <div class='col-sm-5'>" +
        "                                   <input type='text' class='form-control' name='alias_name' placeholder='连接的容器名称(必填)'>" +
        "                               </div>" +
        "                               <div class='col-sm-5'>" +
        "                                   <input type='text' class='form-control' name='host_name' placeholder='在容器中的名称(必填)'>" +
        "                               </div>" +
        "                           </div>" );
});
///////////////判断数据卷容器//////////////
$("#check_volume_from").click(function(){
    $("#volume_from_select").show()
    $("#check_volume_from").hide()
    $("#volume_from_add").show()
});


