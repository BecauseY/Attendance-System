function firstPage3(){
    hide3();
    currPageNum3 = 1;
    showCurrPage3(currPageNum3);
    showTotalPage3();
    for(i = 1; i < pageCount3 + 1; i++){
        blockTable3.rows[i].style.display = "";
    }

    firstText3();
    preText3();
    nextLink3();
    lastLink3();
}

function prePage3(){
    hide3();
    currPageNum3--;
    showCurrPage3(currPageNum3);
    showTotalPage3();
    var firstR = firstRow3(currPageNum3);
    var lastR = lastRow3(firstR);
    for(i = firstR; i < lastR; i++){
        blockTable3.rows[i].style.display = "";
    }

    if(1 == currPageNum3){
        firstText3();
        preText3();
        nextLink3();
        lastLink3();
    }else if(pageNum3 == currPageNum3){
        preLink3();
        firstLink3();
        nextText3();
        lastText3();
    }else{
        firstLink3();
        preLink3();
        nextLink3();
        lastLink3();
    }

}

function nextPage3(){
    hide3();
    currPageNum3++;
    showCurrPage3(currPageNum3);
    showTotalPage3();
    var firstR = firstRow3(currPageNum3);
    var lastR = lastRow3(firstR);
    for(i = firstR; i < lastR; i ++){
        blockTable3.rows[i].style.display = "";
    }

    if(1 == currPageNum3){
        firstText3();
        preText3();
        nextLink3();
        lastLink3();
    }else if(pageNum3 == currPageNum3){
        preLink3();
        firstLink3();
        nextText3();
        lastText3();
    }else{
        firstLink3();
        preLink3();
        nextLink3();
        lastLink3();
    }
}

function lastPage3(){
    hide3();
    currPageNum3 = pageNum3;
    showCurrPage3(currPageNum3);
    showTotalPage3();
    var firstR = firstRow3(currPageNum3);
    for(i = firstR; i < numCount3 + 1; i++){
        blockTable3.rows[i].style.display = "";
    }

    firstLink3();
    preLink3();
    nextText3();
    lastText3();
}

// 计算将要显示的页面的首行和尾行
function firstRow3(currPageNum3){
    return pageCount3*(currPageNum3 - 1) + 1;
}

function lastRow3(firstRow){
    var lastRow = firstRow + pageCount3;
    if(lastRow > numCount3 + 1){
        lastRow = numCount3 + 1;
    }
    return lastRow;
}

function showCurrPage3(cpn){
    currPageSpan3.innerHTML = cpn;
}

function showTotalPage3(){
    pageNumSpan3.innerHTML = pageNum3;
}

//隐藏所有行
function hide3(){
    for(var i = 1; i < numCount3 + 1; i ++){
        blockTable3.rows[i].style.display = "none";
    }
}

//控制首页等功能的显示与不显示
function firstLink3(){firstSpan3.innerHTML = "<a href='javascript:firstPage3();'>First</a>";}
function firstText3(){firstSpan3.innerHTML = "First";}

function preLink3(){preSpan3.innerHTML = "<a href='javascript:prePage3();'>Pre</a>";}
function preText3(){preSpan3.innerHTML = "Pre";}

function nextLink3(){nextSpan3.innerHTML = "<a href='javascript:nextPage3();'>Next</a>";}
function nextText3(){nextSpan3.innerHTML = "Next";}

function lastLink3(){lastSpan3.innerHTML = "<a href='javascript:lastPage3();'>Last</a>";}
function lastText3(){lastSpan3.innerHTML = "Last";}