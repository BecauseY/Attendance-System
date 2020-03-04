function changezt() {
     document.getElementById(zhuangtailan.innerHTML="签到状态：已签到");

}

function changezt2() {
     document.getElementById(zhuangtailan2.innerHTML="签退状态：已签退");

}

function submitForm(){
    $('#SQ').ajaxSubmit(function (message) {
        console.log(message);
        document.getElementById(shenqingliyou.innerHTML="");
        alert("提交成功！");
    });
    return false

}



function jlrefresh() {
    var tbody= document.getElementById("jltable");

     $.ajax({
            url:'/record',
            type:'GET',
            dataType: 'json',
            success:function(u1){
                if(u1){

                    var str = "";
                    for (i in u1){
                        str += "<tr class=\"data-table-row\">"+
                            "<td><div class=\"datagrid-cell cell-c7\"><div>"+u1[i][0]+"</div></div></td>"+
                            "<td><div class=\"datagrid-cell cell-c7\"><div>"+u1[i][1]+"</div></div></td>"+
                            "<td><div class=\"datagrid-cell cell-c7\"><div>"+u1[i][2]+"</div></div></td>"+
                            "<td><div class=\"datagrid-cell cell-c7\"><div>"+u1[i][3]+"</div></div></td>"+
                            "</tr>";
                    }
                    tbody.innerHTML=str;
                }
            },
            error:function(){
                alert("错误！！");
            }
        });
    
}

function xxrefresh() {
    var tbody= document.getElementById("xxtable");

     $.ajax({
            url:'/xiaoxi',
            type:'GET',
            dataType: 'json',
            success:function(u2){
                if(u2){
                    var str = "";
                    for (i in u2){
                        str += "<tr class=\"data-table-row\">" +
                            "<td><div class=\"datagrid-cell cell-c6\"><div>"+u2[i][0]+"</div></div></td>"+
                            "<td><div class=\"datagrid-cell cell-c6\"><div>"+u2[i][1]+"</div></div></td>"+
                            "<td><div class=\"datagrid-cell cell-c6\"><div>"+u2[i][2]+"</div></div></td>"+
                            "<td><div class=\"datagrid-cell cell-c6\"><div>"+u2[i][3]+"</div></div></td>"+
                            "</tr>";
                    }
                    tbody.innerHTML=str;

                }


            },
            error:function(){
                alert("错误！！");
            }
        });

}


