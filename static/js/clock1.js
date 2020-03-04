window.onload=function(){
    var clocknew=document.getElementById('clock1');
    //画刻度
    function drawMark(){
        var w,h;
        for(var i=0;i<60;i++){
            var div=document.createElement("div");

            if(i%5==0){
                var span=document.createElement("span");
                w=4;h=12
            }else{
                w=4;h=4
            }
    div.style.cssText="width:"+w+"px;height:"+h+"px;background:#DEE2EB;position:absolute;border-radius:2px;top:0;left:0;transform:translateX("+(300-w)/2+"px) rotate("+i*6+"deg);transform-origin:"+(w/2)+"px 150px"
            clocknew.appendChild(div)
            span.style.cssText="width:10px;height:10px;font-size:24px;color:#DEE2EB;position:absolute;border-radius:2px;top:10px;left:0;transform:translateX(145px) rotate("+(i+.5)*6+"deg);transform-origin:5px 140px"
            span.innerHTML=(i+1)/5
            clocknew.appendChild(span)
        }
    }
    //画指针
    function drawPointer(w,h,c,a){
        var w=w||6;
         var h=h||50;
        var c=c||"#999";
         var a=a||10
        var div=document.createElement("div");
    div.style.cssText="width:"+w+"px;height:"+h+"px;background:"+c+";position:absolute;left:"+(300/2)+"px;top:"+(150-h/2)+"px;border-radius:5px;transform:rotate("+a+"deg);transform-origin:left center"
        clocknew.appendChild(div);
        return div;
    }
    drawMark();
    var time=new Date();
    var h=drawPointer(75,8,"#fff",time.getHours()*30+time.getMinutes()*6/12-90);
    var m=drawPointer(100,6,"#fff",time.getMinutes()*6-90);
    var s=drawPointer(130,4,"#EE6C3D",time.getSeconds()*6-90);
    setInterval(function(){
        var time=new Date();
        h.style.transform="rotate("+(time.getHours()*30+time.getMinutes()*6/12-90)+"deg)";
        m.style.transform="rotate("+(time.getMinutes()*6-90)+"deg)"
        s.style.transform="rotate("+(time.getSeconds()*6-90)+"deg)"
    },1000)



    var hours=document.getElementsByTagName("select")[0].value;
    var minutes=document.getElementsByTagName("select")[1].value;
    var seconds=document.getElementsByTagName("select")[2].value;
    function setClock(){
        var time = new Date();
        var th = time.getHours();
        var tm = time.getMinutes();
        var ts = time.getSeconds();
        var d1=(th>=hours)&&(tm>=minutes)&&(ts>=seconds);
        var d2=(th>=hours)&&(tm>=minutes);
        var d3=th>hours;
        if(d1||d2||d3){
            clocknew.style.animation="shake 1s linear alternate infinite running"
        }else{
            clocknew.style.animation=""
        }
    }
}
