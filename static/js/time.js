//js 获取当前时间
function fnDate(){
var oDiv=document.getElementById("time");
var date=new Date();
var month=date.getMonth();//当前月份
var data=date.getDate();//天
var hours=date.getHours();//小时
var minute=date.getMinutes();//分
var second=date.getSeconds();//秒
var time=fnW((month+1))+"月"+fnW(data)+"日"+""+fnW(hours)+":"+fnW(minute)+":"+fnW(second);
oDiv.innerHTML=time;
}
//补位 当某个字段不是两位数时补0

function fnDate2(){
var oDiv2=document.getElementById("time2");
var date2=new Date();
var month2=date2.getMonth();//当前月份
var data2=date2.getDate();//天
var hours2=date2.getHours();//小时
var minute2=date2.getMinutes();//分
var second2=date2.getSeconds();//秒
var time2=fnW((month2+1))+"月"+fnW(data2)+"日"+""+fnW(hours2)+":"+fnW(minute2)+":"+fnW(second2);
oDiv2.innerHTML=time2;
}

function fnW(str){
var num;
str>=10?num=str:num="0"+str;
return num;
}





