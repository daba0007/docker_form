

$(function () {
    //1.初始化Table
    var oTable = new image_Table();
    oTable.Init();
    var oTable2 = new container_Table();
    oTable2.Init();
    //2.初始化Button的点击事件
    /* var oButtonInit = new ButtonInit();
    oButtonInit.Init(); */

});

var image_Table = function () {
    var oTableInit = new Object();
    oTableInit.Init = function () {
        $('#image_table').bootstrapTable({
        striped: true,                      //是否显示行间隔色
        pagination: true,                   //是否显示分页（*）
        sortable: true,                     //是否启用排序
        sortOrder: "asc",                   //排序方式
        pageNumber: 1,                       //初始化加载第一页，默认第一页
        pageSize: 5,                         //每页的记录行数（*）
        pageList: [5, 10],                   //可供选择的每页的行数（*）
        search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
        strictSearch: true,
        showColumns: false,                  //是否显示所有的列
        showRefresh: true,                  //是否显示刷新按钮
        minimumCountColumns: 2,             //最少允许的列数
        clickToSelect: true,                //是否启用点击选中行
        showToggle: false,                    //是否显示详细视图和列表视图的切换按钮
        formatLoadingMessage: function () {
            return "请稍等，镜像数据正在加载中...";
          },
          formatNoMatches: function () {  //没有匹配的结果
            return '没有相关的镜像信息';
          },
        url: "/image_table",               //请求的数据
        cache: false,
        toolbar: '#toolbar',                //定义任务栏
        method: 'get',                      //请求方式（*）
        dataType: "json",                   // 服务器返回的数据类型
        sidePagination: 'client',
        queryParams: oTableInit.queryParams,
        columns: [{
                checkbox: true
            }, {
                field: 'id',
                title: '镜像id'
            }, {
                field: 'repository',
                title: '镜像标签'
            }, {
                field: 'tag',
                title: '版本'

            }, {
                field: 'created',
                title: '创建时间'
            }, {
                field: 'size',
                title: '大小（Kb）'
            },]
        });
    };
    return oTableInit;
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            search:params.search
        };
        return temp;
    };
    return oTableInit;
}

var container_Table = function () {
    var oTableInit = new Object();
    oTableInit.Init = function () {
        $('#container_table').bootstrapTable({
            striped: true,                      //是否显示行间隔色
            pagination: true,                   //是否显示分页（*）
            sortable: true,                     //是否启用排序
            sortOrder: "asc",                   //排序方式
            pageNumber: 1,                       //初始化加载第一页，默认第一页
            pageSize: 5,                       //每页的记录行数（*）
            pageList: [5, 10],                   //可供选择的每页的行数（*）
            search: true,                       //是否显示表格搜索，此搜索是客户端搜索，不会进服务端，所以，个人感觉意义不大
            strictSearch: true,
            showColumns: false,                  //是否显示所有的列
            
            uniqueId: "id",
            showRefresh: true,                  //是否显示刷新按钮
            minimumCountColumns: 2,             //最少允许的列数
            clickToSelect: true,                //是否启用点击选中行
            formatLoadingMessage: function () {
                return "请稍等，容器数据正在加载中...";
              },
              formatNoMatches: function () {  //没有匹配的结果
                return '没有相关的容器信息';
              },
            url: "/container_table",               //请求的数据
            cache: false,
            toolbar: '#toolbar2',                //定义任务栏
            method: 'get',                      //请求方式（*）
            dataType: "json",                   // 服务器返回的数据类型
            sidePagination: 'client',
            queryParams: oTableInit.queryParams,
            columns: [{
                checkbox: true
            }, {
                field: 'id',
                title: '容器id',
                sortable : true,
            }, {
                field: 'con_port',
                title: '容器端口',
                sortable : true
            }, {
                field: 'name',
                title: '容器名',
                sortable : true

            }, {
                field: 'created',
                title: '创建时间',
                sortable : true
            }, {
                field: 'status',
                title: '状态',
                sortable : true
            },{
                field: 'image',
                title: '镜像',
                sortable : true
            },{
                field: 'command',
                title: '容器中命令',
                sortable : true
            },{
                field: 'button',
                title: '容器操作',
                events:container_operate,
                formatter:add_container_operate,
            },]
        });
    };
    return oTableInit;
    oTableInit.queryParams = function (params) {
        var temp = {   //这里的键的名字和控制器的变量名必须一直，这边改动，控制器也需要改成一样的
            limit: params.limit,   //页面大小
            offset: params.offset,  //页码
            search:params.search
        };
        return temp;
    };
    return oTableInit;
}

